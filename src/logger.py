import json
from datetime import datetime


def write_to_json(path_to_log, data):
    with open(path_to_log, "r+", encoding='utf-8') as f:
        try:
            json_data = json.load(f)
        except Exception as e:
            print(e)
            print("Json file is empty")
            json_data = []
        json_data.append(data)
        f.seek(0)
        json.dump(json_data, f, indent=4)
    return


def create_data(typ, chat_id, from_user, path_to_log, date, reason):
    date = date.strftime("%d/%m/%Y %H:%M:%S")
    data = {
        "type": f"[{typ}]",
        "chat_id": chat_id,
        "from_user": from_user,
        "reason": reason,
        "date": date
    }
    return data


class Logger:
    def __init__(self):
        pass

    # @staticmethod
    def logit(self, typ, chat_id, from_user, reason, path_to_log):
        date = datetime.now()
        log = f"\n[{date}] | {chat_id} | {from_user} | {reason} | [{typ}]"
        with open(path_to_log, "a") as f:
            f.write(log)
        data = create_data("INFO", chat_id, from_user, path_to_log, date, reason)
        write_to_json("../logs/log.json", data)
        return
