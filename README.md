# 👍👎 Thumbs Vote - Gesture Detection App

โปรแกรมตรวจจับท่าทางนิ้วโป่งผ่าน webcam เพื่อโหวตผ่านหรือไม่ผ่าน

## Features ✨

- 🎥 ตรวจจับท่าทาง Real-time ผ่าน webcam
- 👍 **นิ้วโป่งขึ้น** = PASS (ผ่าน)
- 👎 **นิ้วโป่งลง** = REJECT (ไม่ผ่าน)
- 📊 บันทึกผลโหวตแบบ Real-time
- 🎨 UI ที่สวยงามและใช้งานง่าย
- ⚡ ความแม่นยำสูงด้วย MediaPipe

## Installation 📦

### Requirements
- Python 3.7+
- Webcam
- pip

### Setup

```bash
# Clone this repository
git clone https://github.com/Pwai1G/thumbs-vote.git
cd thumbs-vote

# Install dependencies
pip install -r requirements.txt
```

## Usage 🚀

```bash
# Run the application
python thumbs_vote.py
```

### Controls ⌨️

| Key | Action |
|-----|--------|
| `q` | Quit/Exit |
| `r` | Reset vote counts |

### How to Use 👨‍💻

1. Run the program
2. Face your webcam
3. **Thumbs UP** ☝️ → Vote counts as PASS
4. **Thumbs DOWN** 👎 → Vote counts as REJECT
5. The app counts votes in real-time
6. Press 'q' to exit and see final results

## What Happens 🎬

- ✅ Your hand is detected and tracked
- ✅ Gesture is analyzed (thumbs up/down)
- ✅ Vote is counted (with cooldown to prevent spam)
- ✅ Results displayed on screen in real-time
- ✅ Final results shown when you exit

## Tips 💡

- Make sure lighting is good
- Keep your hand clearly visible
- Hold the gesture for about 1 second for detection
- Stand 60cm away from webcam for best results
- Other fingers should be curled when showing thumbs

## Technical Stack 🛠️

- **OpenCV** - Video capture and image processing
- **MediaPipe** - Hand detection and tracking
- **NumPy** - Numerical computations

## License 📝

MIT License

---

Made with ❤️ by Pwai1G