# Import the geojson module for loading GeoJSON data
import geojson

# Define a function to extract bounding boxes from a GeoJSON file
def extractBBox(file):

    # Load the GeoJSON file and extract the 'features' field, which contains the geometric data
    features = geojson.load(file)['features']

    # Get the number of features in the GeoJSON data
    num_features = len(features)

    # Initialize an empty list to hold the bounding boxes
    bboxList = list()

    # Loop over each feature in the GeoJSON data
    for f in range(num_features):

        # Append the bounding box of the current feature to the list
        # The bounding box is represented as the smallest and largest coordinate values of the feature
        bboxList.append(
            [
                min(features[f]["geometry"]["coordinates"][0]),
                max(features[f]["geometry"]["coordinates"][0])
            ]
        )

    # Return the list of bounding boxes
    return bboxList

# Check if this script is the main program
if __name__== "__main__":

    # Open the GeoJSON file
    with open("testExamples/sample.geojson") as f:

        # Call the extractBBox function to get the bounding boxes of the features in the GeoJSON file
        bboxList = extractBBox(f)

        # Print the list of bounding boxes
        print(bboxList)


    
