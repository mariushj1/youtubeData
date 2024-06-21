import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Definerer channel id
channel_id = "UCgH-5Kph4tE_Q3SyKdo4vGQ"

# Indlæser dataframe
word_count_df = pd.read_csv(f"{channel_id}/word_count.csv")

# Laver dictionary fra dataframe
word_freq = dict(zip(word_count_df['word'], word_count_df['n']))

# Laver wordcloud
image_mask = np.array(Image.open(f"{channel_id}/heart.png"))

wordcloud = WordCloud(background_color="black", mask = image_mask, contour_width=2,
                      contour_color="black", colormap="BuPu_r", width = 800, height = 500).generate_from_frequencies(word_freq)

# Plotter wordcloud
plt.axis("off")
plt.imshow(wordcloud)
 