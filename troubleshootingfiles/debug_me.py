def process_list(l: list) -> list:
    total: int = 0
    for n in l:
        total += n

def main() -> None:
    l: list = [["a", 1, 3.0], ["b", 2, 4.0]]
    m: int

    m = process_list(l)
    print(m)

main()
    
    
