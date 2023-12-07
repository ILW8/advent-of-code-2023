def read_input_from_file(filename: str):
    with open(filename, "r") as infile:
        data = infile.read()
    return data.splitlines()
