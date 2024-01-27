import imageio
filenames = ['draw_test1 vs. average.png', 'draw_test2 vs. average.png']
images = []
nation = 'american'
path = f'../../data/png'
for filename in filenames:
    images.append(imageio.v3.imread(f'{path}/{nation}/{filename}'))

# Save the images as a GIF animation
imageio.mimsave(f'{path}/test_gif.gif', images, duration=0.5)