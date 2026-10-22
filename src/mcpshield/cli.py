import argparse
import json
import sys
from .gateway import MCPShieldGateway, ToolCallRequest

def main():
    parser = argparse.ArgumentParser(description="MCPShield: Model Context Protocol Security Gateway.")
    parser.add_argument("--policy", required=True)
    parser.add_argument("--agent", required=True)
    parser.add_argument("--tool", required=True)
    parser.add_argument("--args", required=True)
    args = parser.parse_args()
    try:
        tool_args = json.loads(args.args)
        gateway = MCPShieldGateway(args.policy)
        req = ToolCallRequest(agent_id=args.agent, tool_name=args.tool, arguments=tool_args)
        result = gateway.evaluate_call(req)
        print(json.dumps(result, indent=2))
        if not result["authorized"]: sys.exit(1)
    except Exception as e:
        print(f"[!] Gateway Error: {e}", file=sys.stderr); sys.exit(1)

if __name__ == "__main__": main()
