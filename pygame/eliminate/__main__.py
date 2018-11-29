from core.main_config import MainConfig

def main():
    configs = MainConfig()
    for monster in configs.monsters:
        print(monster)

if __name__ == "__main__":
    main()