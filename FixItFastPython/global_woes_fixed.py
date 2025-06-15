def double_it(i: int) -> int:
    print(i)
    i = i * 2
    return i

def main() -> None:
    i: int = 10
    i = double_it(i)
    print(i)

if __name__ == "__main__":
    main()
