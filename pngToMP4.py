import glob
from PIL import Image
def sort(x):
    split = x.split('.')
    return int(split[1])

def make_gif():
    frames = glob.glob('/*.png')
    frames = sorted(frames, key=sort)
    frames = [Image.open(image) for image in frames]
    frame_one = frames[0]
    frame_one.save("output.gif", format="GIF", append_images=frames,
        save_all=True, duration=10, loop=0)
    
if __name__ == "__main__":
    make_gif()
