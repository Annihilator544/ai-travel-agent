from pathlib import Path
import sys
import os

# Change to the ai-travel-agent-main directory
os.chdir(Path(__file__).parent / 'ai-travel-agent-main')

# Add current directory to path
sys.path.insert(0, str(Path.cwd()))

if __name__ == "__main__":
    from agents.federated.run_fed import main
    main()