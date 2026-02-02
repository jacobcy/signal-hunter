import argparse
import sys
import json
from src.hunter.scout import HunterConfig, Scout

def main():
    parser = argparse.ArgumentParser(description="Hunter Core - Information Retrieval Engine")
    parser.add_argument("--config", default="config/hunter.yaml", help="Path to configuration file")
    parser.add_argument("--output", help="Path to save output JSON", default=None)
    parser.add_argument("--topic", help="Filter by specific topic name", default=None)
    
    args = parser.parse_args()

    try:
        print(f"Initializing Hunter with config: {args.config}")
        config = HunterConfig(args.config)
        
        # Filter topics if requested
        if args.topic:
            original_count = len(config.topics)
            config.topics = [t for t in config.topics if t.get('name') == args.topic]
            print(f"Filtering topics: '{args.topic}' (Found {len(config.topics)}/{original_count})")
            
        scout = Scout(config)
        
        results = scout.hunt()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            # Print to stdout for piping
            print(json.dumps(results, indent=2))
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
