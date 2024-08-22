import sys
import subprocess


def db_migrate(description: str, force: bool = False) -> None:
    try:
        subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", description], check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error generating migration: {e}")
        sys.exit(1)

    if force or input("Upgrade to head? [y/N]: ").lower() == "y":
        try:
            subprocess.run(["alembic", "upgrade", "head"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error applying migration: {e}")
            sys.exit(1)
    else:
        print("Aborted.")


def main():
    if len(sys.argv) < 2:
        print("Usage: db-migrate <description> [--force]")
        sys.exit(1)

    description = sys.argv[1]
    force = "--force" in sys.argv

    db_migrate(description, force)


if __name__ == "__main__":
    main()
