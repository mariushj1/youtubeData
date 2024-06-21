library(tidyverse)
library(tidytext)
library(stopwords)
library(wordcloud2)
library(RColorBrewer)
library(htmlwidgets)
library(webshot)


# Kanal ID
channel_name <- "Harvest"

# Definerer vejen til mappen
folder_path <- paste0("channels/",channel_name)

youtube_data <- read.csv(file = paste0(folder_path, "/youtube_data.csv"))

# Tæller ord
word_count <- youtube_data %>% 
  unnest_tokens(word, content) %>% 
  count(word, sort = TRUE)

# Fjerner stopord
stopwords_manual <- data.frame(
  word = c("uh", "hey", "yeah", "guys", "time","day","lot","gonna", "god"),
  lexicon = c("SMART", "SMART","SMART","SMART","SMART","SMART","SMART","SMART", "SMART")
)
stopword_df <- rbind(stop_words, stopwords_manual)
word_count <- word_count %>% 
  anti_join(stopword_df, "word")

# Finder de længste ord
word_count$char_count <- nchar(word_count$word)
longest_words_df <- word_count[order(-word_count$char_count), ]

write.csv(word_count, file = paste0(channel_id,"/word_count.csv"), row.names = FALSE)

# Laver wordcloud
# Laver dataframe
wordcloud_df <- word_count %>% 
  select(word, n) %>% 
  top_n(500)
colnames(wordcloud_df) <- c("word", "freq")

# Indlæser figur
#figPath = "/Users/marius/Documents/DataAnalyseProjekter/YoutubeCaptions/UCgH-5Kph4tE_Q3SyKdo4vGQ/tea_shape.png"
#figPath = "/Users/marius/Documents/DataAnalyseProjekter/YoutubeCaptions/UC4xK7CfkqCbBcjXqpJlTIdw/weed_shape.jpeg"
figPath = "/Users/marius/Documents/DataAnalyseProjekter/YoutubeCaptions/UCbvwGzSKXa31P6yDRyoNJnA/fancy_shape.jpg"

# Laver farver
#palette <- c("#e21a36", "#dbb2ae", "#f0f4fd", "#f0f4fd")
#background_color <- "#15170c"

#palette <- c("#dab04a", "#cc8452", "#e3cdb8", "#025172", "#1b8bb0")
#background_color <- "white"

palette <- c("#4b94d6", "#b6c5dc", "#7dd0f0", "#2a547c", "#14366b", "#285da1", "#87afd1", "#2e704c", "#1b6db0")
background_color <- "white"

# Laver wordcloud
wordcloud <- wordcloud2(wordcloud_df,
           figPath = figPath, 
           size = 0.7,
           color = rep_len(palette, nrow(wordcloud_df)), 
           backgroundColor = background_color,
           fontFamily = "Verdana")
wordcloud

# Eksporterer 
saveWidget(wordcloud, "wordcloud.html", selfcontained = FALSE)
webshot("wordcloud.html", "wordcloud.png", vwidth = 2000, vheight = 1400, zoom = 1)


# Laver sentiment analyse på hver video
sentiment_data <- youtube_data %>%
  unnest_tokens(word, content) %>%
  inner_join(get_sentiments("bing")) %>%
  count(title, sentiment) %>%
  spread(sentiment, n, fill = 0) %>%
  mutate(sentiment_score = positive - negative)


View(sentiment_data)
