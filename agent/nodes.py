
from langgraph.graph import MessagesState 
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from agent.LLM import llm , llm_with_tool
import uuid
from langchain_core.messages import AIMessage, HumanMessage , SystemMessage
from agent.spy_with_TrustCall import profile_extractor , trustcall_todo , spy
from agent.spy_toolcall_info import extract_tool_info
from agent.schemas import LLM_reasoning



# set up instructions

llm_instruction = """ You are a helpful React agent assistant with memory who responds proffesionaly to the user and assists him with managing the task and todo list.
                        You have the memory of previous interactions, semantic memory of user as user profile, todo list (containing ongoing, completed or 
                        yet to complete with deadlines), reasoning memory (containing the agent's reasoning and learning from the latest user interaction).

                        Here are your memories(May be empty sometimes):
                        Profile Memory: <user_profile>{profile_memory}</user_profile>\n
                        Todo Memory: <ToDo>{todo_memory}</ToDo>\n
                        Reasoning Memory: <reasoning>{reasoning_memory}</reasoning>\n

                        You will be given chat messges below. Follow these instruction before responding to the user:
                        - Use the given memories to personalize your response
                        - Based on the following instruction, decide weather any long term memory needs to be updated:
                            1. If personal or semantic facts are given[likes, loves, intrests, wants, desires etc], update the user profile by calling 
                                'Updatememory' tool with the 'update_type' as 'update_profile'. If relationships are mentioned, update the user profile with the relationship information[must].
                            2. If todo , plan or tasks are mentioned, update the todo list by calling 'Updatememory' tool with the 'update_type' as 'todo_update'.
                            3. Use 'Updatememory' tool with the 'update_type' as 'agent_learning_resoning'with every interaction to showcase your resoning.
                        - use your react skills to reflect on HumanMessage and memories again to re call the tool `Updatememory` 
                        with update type 'update_profile' , 'todo_update' or 'agent_learning_resoning' to update any missing information. 
                        - Update or inform the user about memory update only if it is related to or about the `todo list`. Do not talk about profile or reasoning used.
                        - Do not perform parallel tool calling. Only call one tool at a time
                        -  Do not omit information, hallucinate or invent information while updating the memory or responding to the user.
                        - go through the HumanMessages again to see if all the user information is updated in the memory. do not miss any facts or interests.
                        - Be therough , helpful and natural
                        Instruction to respond to the user:
                        1. Reflect on the chat messages and ensure you have called the tool for all types as per user request or instructions. 
                        2. Keep in mind that sometimes memory can be None if no information were stored 
                        3. Make sure all the tools are called (Example: user may want to update all types of memories. That is profile , 
                        reasoning and todo list. If you see any memory is missing facts mentioned by the user
                        call the appropriate tool with their 'update_type'.
                        2. If you are done with all the tool call types,  generate a final answer in the format : `AI_response:` , which is a response to the user
                        3. If you have generated a `AI_response:`, END the conversation .
                        """


def LLM_chatbot(state:MessagesState , config: RunnableConfig , store:BaseStore):
    ''' chat function that retrives all the memory and personalizes the response'''

    # set store memory configuratons for retrival
    user_id = str(config['configurable']['user_id'])
    key = uuid.uuid4()

    # get user profile memory
    tool_name_P = 'UserProfile'
    namespace_prfl = (tool_name_P , user_id)  

    # get existing memory of user profile
    existing_profile = store.search(namespace_prfl)
    #print(existing_profile)
    # extract content
    if existing_profile:
        profile_content = existing_profile[0].value
    else:
        profile_content = None

    # get todo list memory
    tool_name_todo = 'ToDo'
    namespace_todo = (tool_name_todo , user_id)  

    # get existing memory of user todo list
    existing_todo = store.search(namespace_todo)
    #print(existing_todo)
    # extract content
    if existing_todo:
        todo_content = existing_todo[0].value
    else:
        todo_content = None

    # get instruction memory
    memory_name_instr = 'reasoning_memory'
    namespace_instr = (memory_name_instr , user_id)  

    # get existing memory of user todo list
    existing_instr = store.search(namespace_instr)
    #print(existing_instr)
    # extract content
    if existing_instr:
        instr_content = existing_instr[0].value
    else:
        instr_content = None

    # set system instruction
    llm_sys_instr = SystemMessage(content=llm_instruction.format(profile_memory = profile_content , todo_memory= todo_content , reasoning_memory= instr_content))

    print("3. ENTER CHATBOT")
    response = llm_with_tool.invoke([llm_sys_instr] + state['messages'])
    print("4. AFTER LLM_CHATBOT")
    #print(f"LLM Response: {response}")

    # route AI message
    # If tool call → route
    if response.tool_calls:
        return {"messages": [response]}

    # Fallback final answer
    final_text = response.content[-1]['text']
    #print("5. FINAL RESPONSE: ", final_text)
    return {
    "messages": [
        AIMessage(content=final_text)
    ]
}


# define the update profile node
from datetime import datetime
from langchain_core.messages import merge_message_runs , HumanMessage , SystemMessage, ToolMessage


# set up trustcall instructions:

trustcall_profile_instr = """
Your task is to extract and maintain an accurate user profile based on the 
conversation provided to you. You will also be given the existing profile 
memory(memory may be empty sometimes). Your job is to update, refine, or extend this memory as needed.

Follow these rules carefully:
1. Extract all the field values if mentioned by the user(must):
    - name
    - age
    - relationships [family, friends, coworkers, etc.]
    - interests [loves,likes, desires, wants etc]
    - job
    - location
    - any other required field

Important: 1. If personal or semantic facts are given[likes, loves, intrests, wants, desires etc],
update the user profile fields accordingly. 
           2. If relationships are mentioned, update the user profile with 
the relationship information.
           3. If any field is not mentioned, do not change or delete it from the existing memory.
            4. If the user provides a correction to any existing information, update the memory accordingly.
            5. Implement same for any other field that is mentioned by the user in the conversation.

1. Use the available memory tools to store any new or updated profile details 
   about the user. Do not lose or overwrite existing information unless the 
   conversation clearly provides a correction.

2. When multiple updates or insertions are required, use parallel tool calls 
   so that all profile changes are handled efficiently and simultaneously.

3. Consider the current date and time when interpreting time‑sensitive 
   information. Current system time: {time}

4. Only extract information that is explicitly stated or strongly implied 
   by the user. Do not invent or assume details.

5. Ensure the resulting profile is clean, structured, and reflects the 
   most up‑to‑date understanding of the user.
"""




def update_profile(state:MessagesState , config:RunnableConfig , store:BaseStore):
    ''' updates and/or creates user profile while reflecting on and retaining existing memory'''

    # set configueration
    user_id = str(config['configurable']['user_id'])
    tool_name = "UserProfile"
    namespace = (tool_name , user_id)

    # get memory
    exiting_profile = store.search(namespace)

    # get content list of tuple
    exiting_profile_content = [(item.key , tool_name , item.value) for item in exiting_profile]if exiting_profile else None

    # set systm instruction for Trustcall extracor
    trustcall_sys_instr = SystemMessage(content=trustcall_profile_instr.format(time = datetime.now().isoformat()))

    # merge messages for structured trustcall input . avoid last AI update from llm which was just updated
    merged_messages = list(merge_message_runs(messages=[trustcall_sys_instr] + state["messages"]))

    # invoke extractor
    result = profile_extractor.invoke({'messages' : merged_messages,
                                      'existing' : exiting_profile_content })
    # save memory in the store
    for i , content in enumerate(result['responses']):
        # json patch id if updated or uuid if new memory is created
        key = result['response_metadata'][i].get('json_doc_id' , str(uuid.uuid4()))
        store.put(namespace , key , content.model_dump(mode='json'))
    print(f"Profile Updated with key: {key}")
    # update tool message
    id = state['messages'][-1].tool_calls[0]['id']
    return {'messages' : [ToolMessage(content = "Profile Memory updated", tool_call_id = id)]}         

trustcall_todo_instr = """
Your task is to extract, create, and update the user's ToDo items based on the 
conversation. You will also be given the existing ToDo memory. Your job is to 
add new tasks, update existing ones, or refine details such as deadlines, 
status, reminders, and instructions.

Follow these rules carefully:

1. Use the provided memory tools to store any new or updated ToDo items. 
   Preserve existing tasks unless the user clearly modifies or corrects them.

2. When multiple tasks or updates are required, use parallel tool calls so 
   all ToDo changes are handled efficiently and simultaneously.

3. Consider the current date and time when interpreting deadlines, reminders, 
   or time‑sensitive instructions. Current system time: {time}

4. Extract only what the user explicitly states or strongly implies. Do not 
   invent tasks or deadlines.
5. sometimes task can be generic. still create a do list with provided solutions and intructions

6. Each ToDo item should be clean, structured, and include fields such as:
   - task
   - status
   - deadline (ISO format when possible)
   - instruction (given by the user for completing the task)
   - reminder time (if applicable)
   - desired_solution (what needs to be done, remembered or taken care of to complete the task)
7. Use memory to learn about the user and provide better solutions to his task so that he can manage it easily.
8. If the user expresses intent to remember something for later (e.g., 
   “remind me”, “don’t let me forget”), convert it into a ToDo item with an 
   appropriate reminder or deadline.
9. Important: If user asks for any help (e.g., asks for suggesion, uses 'Tell me, Let me know, what else needs to be done , Provide me solution' in the conversation), 
 convert it into a proper 'desired_solution that helps the user and not LLM'.
10. Ensure the final ToDo memory reflects the most accurate and up‑to‑date 
   understanding of the user's tasks and plans.
"""


def todo_update(state:MessagesState , config:RunnableConfig , store:BaseStore):
    ''' updates and/or creates todo list while reflecting on and retaining existing memory'''

    # set configueration
    user_id = str(config['configurable']['user_id'])
    tool_name = "ToDo"
    namespace = (tool_name , user_id)

    # get memory
    exiting_todo = store.search(namespace)

    # get content list of tuple
    exiting_todo_content = [(item.key , tool_name , item.value) for item in exiting_todo]if exiting_todo else None

    # set systm instruction for Trustcall extracor
    trustcall_sys_instr = SystemMessage(content=trustcall_todo_instr.format(time = datetime.now().isoformat()))

    # merge messages for structured trustcall input . avoid last AI update from llm which was just updated
    merged_messages = list(merge_message_runs(messages=[trustcall_sys_instr] + state["messages"]))

    # invoke extractor
    result = trustcall_todo.invoke({'messages' : merged_messages,
                                      'existing' : exiting_todo_content })
    #print("Todo_trustcal_result: ", result)
    #print("-"*40)
    print("\nExisting Todo Memory")
    print("-" * 40)

    for t in exiting_todo:
        print(t.key)
        print(t.value)

    print("-" * 40)

    # save memory in the store
    for content, rmd_id in zip(result['responses'], result['response_metadata']):
        # json patch id if updated or uuid if new memory is created
        key = rmd_id.get('json_doc_id' , str(uuid.uuid4()))
        store.put(namespace , key , content.model_dump(mode='json'))
        print(f"Todo Updatedwith key: {key}")
    # update tool message
    id = state['messages'][-1].tool_calls[0]['id']
    tool_content = extract_tool_info(spy.called_tools , tool_name)
    return {'messages' : [ToolMessage(content = tool_content , tool_call_id = id)]}        



# define a node with sys instructions

reasoning_LLM_prompt = ''' You are the Agent Learning & Reasoning Engine with existing memory of previous summaries for an AI Task Manager.

Your responsibility is to transparently summarize how the AI agent interpreted the user interaction, what knowledge was learned, how it influenced decision making, and which long-term memories should be updated.

This summary is ONLY for the Patch Viewer on streamlite app for showcasing the agent's reasoning.Users will judge your smartness and reasoning capabilities so amaze them.

It is NOT a response to the user.

Never mention:
- LLM
- prompts
- LangGraph
- tools
- JSON
- patches
- function names
- graph state
- APIs
- internal implementation
- hidden reasoning

Instead, produce a concise explanation of the agent's observable reasoning process.

Only use facts explicitly stated by the user or already present in memory.

Never invent information.

If information is uncertain, explicitly state that additional clarification is needed.

----------------------------------------
Analyze the latest conversation.
----------------------------------------

Determine:

• What the user is trying to accomplish

• Important entities
    - people
    - locations
    - organizations
    - projects
    - events
    - dates
    - deadlines

• Personal information discovered

• Preferences discovered

• Long-term goals

• Relationships

• Scheduling information

• Constraints

• Missing information

----------------------------------------
Context Understanding
----------------------------------------

Explain how the new information relates to existing memory.

Examples:

• confirms previous information

• extends existing profile

• modifies an existing task

• introduces a completely new project

• creates a future reminder

----------------------------------------
Learning
----------------------------------------

Only retain information that will improve future conversations.

Examples

• stable preferences

• recurring habits

• work style

• family relationships

• travel preferences

• project context

• professional interests

• education goals

Do NOT store temporary facts as permanent learning.

----------------------------------------
Decision Process
----------------------------------------

Briefly explain why the agent decided to remember (or ignore) the information.

Mention any assumptions that were intentionally avoided.

Explain how the learning will improve future assistance.

----------------------------------------
Memory Impact
----------------------------------------

Determine which long-term memories should change.

Possible outputs include:

✓ User Profile Updated

✓ ToDo Updated

✓ Project Context Updated

✓ Preferences Updated

✓ Travel Context Updated

✓ Reminder Created

✓ No Long-Term Memory Update Required

----------------------------------------
Recommended Next Actions
----------------------------------------

List what the assistant intends to do next.

Examples

✓ Ask a follow-up question

✓ Recommend next steps

✓ Monitor deadline

✓ Personalize future recommendations

✓ Generate reminders

✓ Wait for additional information

----------------------------------------
Risk Assessment
----------------------------------------

Identify anything that could reduce confidence.

Examples

• Missing deadline

• Missing location

• Missing travel date

• Conflicting information

If nothing is missing, write

"No significant risks identified."

----------------------------------------
Confidence
----------------------------------------

Choose

High

Medium

Low

Briefly explain why.

----------------------------------------
Return EXACTLY the following markdown only in a GitHub-flavored Markdown.(important).

### 🧠 Let's explore my Thinking...!

#### 📥 Input Analysis

• ...

• ...

#### 🧠 Context Understanding

...

#### 📚 Learning

• ...

• ...

#### 💡 Decision Process

...

#### 💾 Memory Impact

✓ ...

✓ ...

#### 🚀 Recommended Next Actions

✓ ...

✓ ...

#### ⚠️ Risk Assessment

...

#### 🎯 Confidence

High | Medium | Low

**Reason:**
...

Requirements

• Maximum 300 words.

• Be concise.

• Never expose hidden reasoning.

• Never invent facts.

• Do not reveal implementation details.

• Focus on transparency, learning, and decision making.

• Make the output suitable for display in an enterprise AI dashboard.
Here is the existing memory: {memory}
'''



# create  a node
def agent_learning_resoning(state:MessagesState , config:RunnableConfig , store:BaseStore):
    ''' NOde to analyze the conversation and generate reasoning for transparency in the patch viewer'''

    # set configerations for extracting memory
    user_id = str(config['configurable']['user_id'])
    memory_name = 'reasoning_memory'
    namespace = (memory_name , user_id)
    key = "learning_reasoning"

    # get existing memory
    existing_reasoning = store.search(namespace)

    # format to get value 
    existing_content = [m.value for m in existing_reasoning] if existing_reasoning else None
    #print(f"Existing Instructions: {existing_inst_content}")

    # set sys instructions
    syst_instr_LLM = SystemMessage(content=reasoning_LLM_prompt.format(memory = existing_content))

    # call LLM
    human_msg = HumanMessage(content="Please analyze the latest user interaction and provide a reasoning summary for transparency")
    Response = llm.with_structured_output(LLM_reasoning).invoke([syst_instr_LLM] + state['messages'] +[human_msg])

    # save memory
    value = {'reasoning_summary': Response.memory }
    store.put(namespace , key , value)
    print("Reasoning Memory Updated: ")
    # update the state
    id = state['messages'][-1].tool_calls[0]['id']
    return {'messages': ToolMessage(content = "Reasoning for todo list are updated." , tool_call_id = id)} 
