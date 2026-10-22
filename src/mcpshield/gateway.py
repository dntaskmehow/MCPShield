import json
from typing import Dict, Any
from pydantic import BaseModel

class ToolCallRequest(BaseModel):
    agent_id: str
    tool_name: str
    arguments: Dict[str, Any]

class MCPShieldGateway:
    def __init__(self, policy_file: str):
        with open(policy_file, "r", encoding="utf-8") as f:
            self.policy = json.load(f)

    def evaluate_call(self, request: ToolCallRequest) -> Dict[str, Any]:
        agent_rules = self.policy.get(request.agent_id, {"allowed_tools": [], "blocked_patterns": []})
        if request.tool_name not in agent_rules.get("allowed_tools", []):
            return {"authorized": False, "reason": f"Access denied: Agent '{request.agent_id}' not permitted to invoke tool '{request.tool_name}'."}
        for arg_key, arg_val in request.arguments.items():
            val_str = str(arg_val).lower()
            for pattern in agent_rules.get("blocked_patterns", [";", "rm -rf", "drop table", "../../"]):
                if pattern in val_str:
                    return {"authorized": False, "reason": f"Security violation: Malicious pattern '{pattern}' detected in argument '{arg_key}'."}
        return {"authorized": True, "reason": "Request inspected and approved by MCPShield."}
