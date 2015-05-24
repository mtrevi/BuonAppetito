cd "`dirname \"$0\"`"

# cp -f ../scripts/analysis/output/sentence_vs_review_sentiment.csv data
# cp -f ../scripts/analysis/output/review_stars_vs_sentiment_rounded.csv data
# cp -rf ../scripts/analysis/output/food_by_category data
# cp -f ../scripts/analysis/output/food.csv data
# cp -f ../scripts/analysis/output/food_per_review.csv data

rsync -rz --progress --size-only media5:projects/yelpChallenge/output/sentence_vs_review_sentiment.csv data
rsync -rz --progress --size-only media5:projects/yelpChallenge/output/review_stars_vs_sentiment_rounded.csv data
rsync -rz --progress --size-only media5:projects/yelpChallenge/output/food_by_category data
rsync -rz --progress --size-only media5:projects/yelpChallenge/output/food.csv data
rsync -rz --progress --size-only media5:projects/yelpChallenge/output/food_per_review.csv data
# rsync -rz --progress --size-only media5:projects/yelpChallenge/output/kendall_tau_frequent_rounded.csv data
cp -f ../output/kendall_tau_frequent_rounded.csv data
cp -f ../output/kendall_tau_by_business_apriori_rounded.csv data
cp -f ../output/jaccard_by_business_rounded_apriori.csv data
