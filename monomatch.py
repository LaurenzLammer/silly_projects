# import required packages
import cv2
import matplotlib
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
# use matplotlib in non-interactive mode to suppress opening of figure windows
matplotlib.use('Agg')
import numpy
from random import shuffle, sample, choice
import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser(description='Create a deck of 57 dobble cards using 57 images supplied by the user. '
                                             'Please provide a directory containing 57 images. '
                                             'Ideally, pre-crop images to a square format. '
                                             'Otherwise, monomatch.py will crop them to the largest possible central square. '
                                             'Monomatch.py will create 2 new directories next to the one you provided with the added suffixes _sq to store cropped images and _cards to store images of prepared cards with 8 pictures on them. '
                                             'Additionally, monomatch.py can create n pairings of the prepared cards for you to check out the result and try if you like it before printing it. '
                                             'Monomatch will not install required dependencies if they are not already existing. '
                                             'Please use the pip compatible text file monomatch_requirements to install required libraries. ')


parser.add_argument('image_directory', metavar='image_directory', type=str, nargs='?',
                    help='Give the directory containing the 57 images. Default is current directory', default=os.getcwd())
parser.add_argument('-trial', '--trial', action= 'store_true', default=False,
                    help='Add this argument if you want monomatch.py to create a trial set of card pairs.')
parser.add_argument('-ntrial', '--ntrial', action= 'store', type=int, default=50,
                    help='Add this argument to indictae the number of trial set card pairs. Default is 50.')

# handle command line arguments
args = parser.parse_args()
im_dir = Path(args.image_directory)
sq_dir = im_dir.parents[0] / "images_sq"
cards_dir = im_dir.parents[0] / "monomatch_cards"
os.makedirs(sq_dir, exist_ok = True)
os.makedirs(cards_dir, exist_ok = True)

# create a list of lists containing the numbers from 0-6, 7-13, ... 49-55
numbers = [list(range(i*7, i*7+7)) for i in range(8)]
# create a list of 57 cards
# the cards will be lists in which the numbers of the pictures depicted on them will be stored
cards = [[] for k in range(57)]
# allocate the right nu,mbers to the appropriate cards
for n in range(7):
    for m in range(7):
        # add horizontal and vertical lines
        cards[n*7+m].extend([n,m+7])
        # add opblique lines
        for o in range(6):
            cards[n * 7 + m].append(numbers[o+2][(m + n * (6-o)) % 7])
    # add vanishing points, the vanishing points will share the last (the 57th) picture
    cards[49+n] = numbers[n]
    cards[49 + n].append(56)
# add vanishing point of the vanishing points
cards[56] = numbers[7]
cards[56].append(56)

# import 57 images
images = []
# iterate through photos in directory and read them in
for image in os.listdir(str(im_dir)):
    photo = cv2.imread(str(im_dir / image))
    photo_shape = numpy.shape(photo)
    width = photo_shape[1]
    height = photo_shape[0]
    # create cropped images
    if width > height:
        cropped_image = photo[0:height, int((width - height) / 2):int(width - ((width - height) / 2))]
    elif height > width:
        cropped_image = photo[int((height - width) / 2):int(height - ((height - width) / 2)), 0:width]
    else:
        cropped_image = photo
    # save squared images
    cv2.imwrite(str(sq_dir / (image + "_sq.png")), cropped_image)
    # change BGR to RGB colour coding for pyplot
    cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
    # append image to images list
    images.append(cropped_image)

# define function to show and randomly rotate an image
def showrot(image):
    """Plot the image and rotate it if a random 50/50 choice turns out True

            Parameters
            ----------
            image : the image to plot
            """
    if choice([True,False])== True:
        image = cv2.rotate(image, cv2.ROTATE_180)
    plt.imshow(image)

# define function for card creation
def card_creator(images, card, layout, n):
    """Create a customized dobble card.

        Parameters
        ----------
        images : list of 57 images
        card : list of 8 images to be plotted on the card
        layout : number of 1-4 to determine which layout may be used
        n : number of the card
        """
    if layout == 1:
        fig = plt.figure(figsize=(10, 10), frameon=False, layout='constrained')
        spec = gridspec.GridSpec(ncols=5, nrows=5, figure=fig)
        fig.add_subplot(spec[0:2, 0:2])
        showrot(images[card[0]])
        plt.axis('off')
        fig.add_subplot(spec[2:4, 0:2])
        showrot(images[card[1]])
        plt.axis('off')
        fig.add_subplot(spec[0:2, 2:4])
        showrot(images[card[2]])
        plt.axis('off')
        fig.add_subplot(spec[0, 4])
        showrot(images[card[3]])
        plt.axis('off')
        fig.add_subplot(spec[1, 4])
        showrot(images[card[4]])
        plt.axis('off')
        fig.add_subplot(spec[2:, 2:])
        showrot(images[card[5]])
        plt.axis('off')
        fig.add_subplot(spec[4, 0])
        showrot(images[card[6]])
        plt.axis('off')
        fig.add_subplot(spec[4, 1])
        showrot(images[card[7]])
        plt.axis('off')
    elif layout == 2:
        fig = plt.figure(figsize=(10, 10), frameon=False, layout='constrained')
        spec = gridspec.GridSpec(ncols=5, nrows=5, figure=fig)
        fig.add_subplot(spec[0:2, 0:2])
        showrot(images[card[0]])
        plt.axis('off')
        fig.add_subplot(spec[0, 2])
        showrot(images[card[1]])
        plt.axis('off')
        fig.add_subplot(spec[1, 2])
        showrot(images[card[2]])
        plt.axis('off')
        fig.add_subplot(spec[2:, :3])
        showrot(images[card[3]])
        plt.axis('off')
        fig.add_subplot(spec[0,3])
        showrot(images[card[4]])
        plt.axis('off')
        fig.add_subplot(spec[0,4])
        showrot(images[card[5]])
        plt.axis('off')
        fig.add_subplot(spec[1:3,3:])
        showrot(images[card[6]])
        plt.axis('off')
        fig.add_subplot(spec[3:, 3:])
        showrot(images[card[7]])
        plt.axis('off')
    elif layout == 3:
        fig = plt.figure(figsize=(10, 10), frameon=False, layout='constrained')
        spec = gridspec.GridSpec(ncols=5, nrows=5, figure=fig)
        fig.add_subplot(spec[0:3, 0:3])
        showrot(images[card[0]])
        plt.axis('off')
        fig.add_subplot(spec[0:2, 3:])
        showrot(images[card[1]])
        plt.axis('off')
        fig.add_subplot(spec[2, 3])
        showrot(images[card[2]])
        plt.axis('off')
        fig.add_subplot(spec[2, 4])
        showrot(images[card[3]])
        plt.axis('off')
        fig.add_subplot(spec[3:,:2])
        showrot(images[card[4]])
        plt.axis('off')
        fig.add_subplot(spec[3,2])
        showrot(images[card[5]])
        plt.axis('off')
        fig.add_subplot(spec[4,2])
        showrot(images[card[6]])
        plt.axis('off')
        fig.add_subplot(spec[3:, 3:])
        showrot(images[card[7]])
        plt.axis('off')
    elif layout == 4:
        fig = plt.figure(figsize=(10, 10), frameon=False, layout='constrained')
        spec = gridspec.GridSpec(ncols=5, nrows=5, figure=fig)
        fig.add_subplot(spec[0:3, 0:3])
        showrot(images[card[0]])
        plt.axis('off')
        fig.add_subplot(spec[0:2, 3:])
        showrot(images[card[1]])
        plt.axis('off')
        fig.add_subplot(spec[2, 3])
        showrot(images[card[2]])
        plt.axis('off')
        fig.add_subplot(spec[2, 4])
        showrot(images[card[3]])
        plt.axis('off')
        fig.add_subplot(spec[3,0])
        showrot(images[card[4]])
        plt.axis('off')
        fig.add_subplot(spec[4,0])
        showrot(images[card[5]])
        plt.axis('off')
        fig.add_subplot(spec[3:,1:3])
        showrot(images[card[6]])
        plt.axis('off')
        fig.add_subplot(spec[3:, 3:])
        showrot(images[card[7]])
        plt.axis('off')
    # save the card as a png.file
    plt.savefig(str(cards_dir / (str(n) + ".png")))

# create the 57 cards
finished_cards = []
for n in range(57):
    # shuffle image indices on a card to randomise the placement of the images
    shuffle(cards[n])
    # randomly choose one layout for the card
    lay = choice([1,2,3,4])
    # create the card
    card_creator(images = images, card = cards[n], layout = lay, n = n)

# if option -trial is used, -ntrial card pairings shall be produced to give the user a accurate representation of the result before printing
if args.trial:
    # create dir of card pairings
    pairs_dir = im_dir.parents[0] / "monomatch_card_pairs"
    os.makedirs(pairs_dir, exist_ok=True)
    # load the finished cards
    # import 57 images
    finished_cards = []
    # iterate through photos in directory, read them in and change colour coding for pyplot
    for image in os.listdir(str(cards_dir)):
        im = cv2.cvtColor(cv2.imread(str(cards_dir / image)), cv2.COLOR_BGR2RGB)
        finished_cards.append(im)
    # create ntrial sets of two cards to test-play on a screen
    for n in range(args.ntrial):
        fig = plt.figure(figsize=(20, 10))
        card_nos = sample(range(57), 2)
        fig.add_subplot(1, 2, 1)
        plt.imshow(finished_cards[card_nos[0]])
        plt.axis('off')
        plt.tight_layout()
        fig.add_subplot(1, 2, 2)
        plt.imshow(finished_cards[card_nos[1]])
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(str(pairs_dir / (str(n) + ".png")))


