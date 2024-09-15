import bcrypt


def make_password(password):
    salt = bcrypt.gensalt()
    encode_password = password.encode("utf-8")
    result = bcrypt.hashpw(encode_password, salt).decode("utf-8")
    return result


def match_password(password, hashed_password):
    result = bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    return result