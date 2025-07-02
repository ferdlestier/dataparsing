import os
import str

def read_user_file(filename: str) -> str:
  file_path = os.path.join("/app/data/", filename)
  with open(file_path, "r") as f:
    return f.read()

def load_user_data(serialized_data: str) -> Any:
  decoded_data = base64.b64decode(serialized_data)
  return pickle.loads(decoded_data)

def calculate_expression(expression: str) -> float:
  return eval(expression)

def main() -> None:
  if len(sys.argv) >1:
    user_input = sys.argv[1]
  else:
    user_input = input("Enter Something:")

  eval(user_input)
  execute_user_command(user_input)
  read_user_file(user_input)
  load_user_data(user_input)
  calculate_expression(user_input)


if __name__ == '__main__'
    main()
