# 🤖 My Robot Storybook Maker (LinkedIn AI Poster)

Hi there! This is a magic machine that helps you share cool stories about robots (AI) with your friends on LinkedIn. 

Imagine you have a robot helper that:
1. 🕵️ **The Scout (Serper):** Looks around the internet to see what robots are doing today.
2. ✍️ **The Writer (Groq):** Writes a fun story about what it found.
3. 📸 **The Photographer (Pexels):** Picks a pretty picture to go with the story.
4. 📮 **The Mailman (LinkedIn):** Puts the story on your LinkedIn wall so everyone can see!

---

## 🔑 Magic Keys (What you need)

To make the robot work, you need 5 "Magic Keys". These are special codes (API keys) that you put in a secret file called `.env` inside the `config` folder.

1. **The Brain Key (Groq API Key):** 
   - *What it does:* Helps the robot think and write stories.
   - *Where to get it:* [Groq Console](https://console.groq.com/)

2. **The Scout Key (Serper API Key):** 
   - *What it does:* Helps the robot search the big internet for news.
   - *Where to get it:* [Serper.dev](https://serper.dev/)

3. **The Camera Key (Pexels API Key):** 
   - *What it does:* Helps the robot find beautiful pictures for your posts.
   - *Where to get it:* [Pexels API](https://www.pexels.com/api/)

4. **The Post Office Key (LinkedIn Access Token):** 
   - *What it does:* This is the key to your LinkedIn house so the robot can post for you.
   - *Where to get it:* [LinkedIn Developers Portal](https://www.linkedin.com/developers/)

5. **The ID Card (LinkedIn Person URN):** 
   - *What it does:* This tells LinkedIn exactly which person is posting (it's like your digital name tag).
   - *Where to get it:* Found via the LinkedIn API "me" endpoint.

---

## 🚀 How to wake up the robot

1. **Give it Tools:** Open your black command box and type:
   ```bash
   pip install -r requirements.txt
   ```
2. **Give it the Keys:** Put your Magic Keys into `config/.env`.
3. **Press Start:** Type this to send a post right now:
   ```bash
   python core/scheduler.py
   ```

---

## 📅 What does the robot talk about?
The robot has a schedule so it never gets bored:
- **Monday:** 🛠️ **Cool Tools** (New robot toys)
- **Tuesday:** 🏥 **Doctors & Robots** (How AI helps sick people)
- **Wednesday:** 💰 **Money & Robots** (Banks and AI)
- **Thursday:** 🏢 **Work & Robots** (Helping people at their jobs)
- **Friday:** 🧪 **New Science** (Advanced robot research)
- **Saturday:** ⌚ **Watches & Health** (AI in your watch and fitness)
- **Sunday:** 📰 **Weekly News** (A big recap of the whole week)

---

### 👨‍💼 For Grown-ups (Technical Details)
- **Language:** Python 3.10+
- **Main Brain:** Groq (Llama 3 70B)
- **Search:** Serper.dev API
- **Images:** Pexels API (Stock photos)
- **History:** Stores posts in `data/history.db` so it doesn't repeat itself.
- **Logs:** If the robot gets a "tummy ache" (error), check the `logs/` folder!
