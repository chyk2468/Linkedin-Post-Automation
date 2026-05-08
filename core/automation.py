import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

import datetime
import time
from config.config import DAY_TOPICS
from core.fetcher import gather_research
from core.summarizer import generate_content
from core.formatter import format_post
from core.image_gen import generate_image
from core.publisher import post_to_linkedin
from core.logger import log_success, log_error, is_duplicate

class AutomationPipeline:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    def run(self, day_index: int = None):
        if day_index is None:
            day_index = datetime.datetime.now().weekday()
        
        try:
            # 1-5. Preparation
            data = self.prepare_post(day_index)
            if not data:
                return False

            if self.dry_run:
                print("\n🧪 [DRY RUN] Post Content:")
                print("-" * 30)
                print(data['final_post'])
                print("-" * 30)
                print(f"🧪 [DRY RUN] Image would be: {data['image_path']}")
                return True

            # 6. Publishing
            return self.publish_post(data)

        except Exception as e:
            log_error(str(e), {"day_index": day_index})
            return False

    def prepare_post(self, day_index: int):
        topic_config = DAY_TOPICS[day_index]
        print(f"\n🌟 Pipeline Preparing for: {topic_config['name']}")

        # 1. Research
        research_brief = gather_research(topic_config)
        
        # 2. Content Generation
        raw_data = generate_content(research_brief, topic_config)
        
        # 3. Duplicate Protection
        if is_duplicate(raw_data['topic']):
            print(f"⏭️ Skipping: Topic '{raw_data['topic']}' was already posted.")
            return None

        # 4. Formatting
        final_post = format_post(raw_data, topic_config)
        
        # 5. Image Sourcing (Pexels)
        image_path, attribution = generate_image(raw_data['image_prompt'], raw_data['topic'])
        
        # Append attribution to post if available
        if attribution:
            final_post += f"\n\n📸 {attribution}"
        
        return {
            "day_index": day_index,
            "topic_config": topic_config,
            "raw_data": raw_data,
            "final_post": final_post,
            "image_path": image_path
        }

    def publish_post(self, data: dict):
        # 6. Publishing with Retries
        post_id = self.attempt_publish(data['final_post'], data['image_path'])
        
        if post_id:
            # 7. Logging
            log_success({
                "day": datetime.datetime.now().strftime("%A"),
                "topic": data['raw_data']['topic'],
                "post": data['final_post'],
                "post_id": post_id,
                "image": data['image_path'],
                "image_prompt": data['raw_data']['image_prompt']
            })
            return True
        return False

    def attempt_publish(self, post_text, image_path, retries=3):
        for i in range(retries):
            try:
                return post_to_linkedin(post_text, image_path)
            except Exception as e:
                print(f"⚠️ Publish attempt {i+1} failed: {e}")
                if i < retries - 1:
                    time.sleep(60) # Wait 1 minute before retry
        return None

def main():
    import sys
    pipeline = AutomationPipeline(dry_run="--test" in sys.argv)
    
    target_day = None
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        target_day = int(sys.argv[1])
    
    pipeline.run(day_index=target_day)

if __name__ == "__main__":
    main()
