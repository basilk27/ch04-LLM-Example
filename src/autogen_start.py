from autogen import ConversableAgent, UserProxyAgent, config_list_from_json

# load the configuration list from the OAI_CONFIG_LIST file
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

# create the agent that uses the LLM
assistant_agent = ConversableAgent(
    "assistant_agent",
    llm_config = {"config_list": config_list}
)

# create the user agent in the conversation
user_agent = UserProxyAgent(
    "user_agent",
    code_execution_config = {
        "work_dir": "working",
        "use_docker": False
    },
    human_input_mode = "ALWAYS",
    is_termination_msg = lambda x: x.get("content", "")
    .rstrip()
    .endswith("TERMINATE")
)

# start the conversation
results = user_agent.initiate_chat(assistant_agent, message="write a solution for fizz buzz in one line?")
