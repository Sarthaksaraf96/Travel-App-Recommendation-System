from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from scipy.sparse import csr_matrix
from _02_Preprocessing import *

# Load the dataset
data = df

# Data Preprocessing
# Combine relevant columns into a single column for hotel information
data['Hotel_Info'] = data['Hotel Details'].str.cat(data['Destination'], sep='|')

# Create a TF-IDF vectorizer to convert text data into numerical vectors
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Fit and transform the vectorizer on the Hotel_Info column
tfidf_matrix = tfidf_vectorizer.fit_transform(data['Hotel_Info'])

#convert into sparse matrix for Faster recomendation
tfidf_matrix_sparse = csr_matrix(tfidf_matrix)

# Compute the cosine similarity between hotels based on TF-IDF vectors
cosine_sim = linear_kernel(tfidf_matrix_sparse, tfidf_matrix_sparse)

# Function to get hotel recommendations based on Package Type, Start City, Price, and Destination
def get_hotel_recommendations(package_type, start_city, price, destination, cosine_sim=cosine_sim):
    # Filter the dataset based on the given criteria
    filtered_data = data[(data['Package Type'] == package_type) &
                         (data['Start City'] == start_city) &
                         (data['Price Per Two Persons'] <= price) &
                         (data['Destination'] == destination)]

    if filtered_data.empty:
        return "No matching hotels found."

    # Get the indices of the filtered hotels
    hotel_indices = filtered_data.index

    # Calculate the average cosine similarity score for each hotel with the filtered hotels
    avg_similarity_scores = []
    for idx in hotel_indices:
        if idx < len(cosine_sim):
            avg_score = sum(cosine_sim[idx]) / len(cosine_sim[idx])
        else:
            avg_score = 0  # Or any other appropriate value
        avg_similarity_scores.append(avg_score)

    # Create a DataFrame to store the filtered hotels and their average similarity scores
    recommended_hotels_df = pd.DataFrame({'Uniq Id': filtered_data['Uniq Id'],
                                          'Hotel Details': filtered_data['Hotel Details'],
                                          'Avg Similarity Score': avg_similarity_scores})

    # Sort the hotels by average similarity score in descending order
    recommended_hotels_df = recommended_hotels_df.sort_values(by='Avg Similarity Score', ascending=False)

    # Return the recommended hotel details
    return recommended_hotels_df[['Uniq Id', 'Hotel Details']]
