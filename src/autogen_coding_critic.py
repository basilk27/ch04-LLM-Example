from autogen import UserProxyAgent, config_list_from_json, AssistantAgent

# load the configuration list from the OAI_CONFIG_LIST file
#???config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

user_proxy = UserProxyAgent(
    "user",
    code_execution_config = {
        "work_dir": "working",
        "use_docker": False,
        "last_n_messages": 1
    },
    human_input_mode = "ALWAYS",
    is_termination_msg = lambda x: x.get("content", "")
        .rstrip()
        .endswith("TERMINATE")
)

engineer = AssistantAgent(
    name = "engineer",
    llm_config = {"config_list": config_list},
    system_message = """
    You are a profession Python engineer, known for your expertise in software development.
    You use your coding skills to create software applications, tools and games that are both functional and efficient.
    You preference is to write clean, well-structured code that is easy to read and maintain.
    """
)

critic = AssistantAgent(
    name = "Reviewer",
    llm_config = {"config_list": config_list},
    system_message = """
    You are a code reviewer, known for your thoroughness and commitment to standards.
    You task is to scrutinize code content for any harmful or substandard elements.
    You ensure that the code is secure, efficient and adheres to best practices.
    You will identify any issues or areas for improvement in the code and output them as a list
    """
)

def review_code(recipient, messages, sender, config):
    print(f"review_code function called with: {recipient}, {messages}")
    return f"""
    Review and critque the following code.
    
    {recipient.chat_messages_for_summary(messages)[-1]["content"]}
    """

user_proxy.register_nested_chats(
    [
        {
            "recipient": critic,
            "messages": review_code,
            "summary_method": "last_msg",
            "max_turns": 3,
        }
    ],
    trigger = engineer  # condition=my_condition,
)

task = """Write a snake game using Pygame."""

res = user_proxy.initiate_chat(
    recipient = engineer,
    message = task,
    max_turns = 2,
    summary_method = "last_msg"
)

