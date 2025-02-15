from imports import *

def create_display():
    image_paths = [
    "media/image1.webp",
    "media/image2.webp",
    ]

    slider = pn.widgets.IntSlider(name="Image Slider", start=0, end=len(image_paths) - 1, step=1, value=0)
    preloaded_images = [None] * len(image_paths)

    def preload_image(index):
        if preloaded_images[index] is None:
            # Simulate loading with a delay
            preloaded_images[index] = image_paths[index]

    def update_image(index):
        # Preload the next image in a separate thread
        next_index = (index + 1) % len(image_paths)
        Thread(target=preload_image, args=(next_index,)).start()
        
        return pn.panel(preloaded_images[index] or image_paths[index], height=1080)

    image_display = pn.bind(update_image, slider)

    disp_component = pn.Column(
        slider,
        image_display
    )

    return disp_component