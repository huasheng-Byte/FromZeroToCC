# todo_manager.py
class TodoManager:
    def __init__(self):
        self.items: list[dict] = []

    def update(self, todos: list | str) -> str:
        validated = []
        # 这里放完整校验逻辑
        if isinstance(todos, list):
            for item in todos:
                if not isinstance(item, dict):
                    raise ValueError("Todo item must be dict")
                if "content" not in item or "status" not in item:
                    raise ValueError("Todo requires content and status")
                if item["status"] not in ["pending", "in_progress", "completed"]:
                    raise ValueError(f"Invalid status {item['status']}")
                if len(item["content"]) < 1:
                    raise ValueError("content cannot be empty")
                validated.append(item)
        else:
            raise ValueError("todos must be list of todo dicts")
        self.items = validated
        return self.render()

    def render(self) -> str:
        if not self.items:
            return "No todos."
        lines = []
        for todo in self.items:
            marker = {
                "pending":      "[ ]",
                "in_progress": "[>]",
                "completed":   "[x]",
            }[todo["status"]]
            lines.append(f"{marker}{todo['content']}")
        done = sum(t["status"] == "completed" for t in self.items)
        lines.append(f"\n({done}/{len(self.items)} completed)")
        return "\n".join(lines)

TODO = TodoManager()
