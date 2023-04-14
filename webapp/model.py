
import random


from tflite_support.task import vision
from tflite_support.task import core
from tflite_support.task import processor



model_path = './models/lite-model_imagenet_mobilenet_v3_large_100_224_classification_5_metadata_1.tflite'

# Initialization
base_options = core.BaseOptions(file_name=model_path)
classification_options = processor.ClassificationOptions(max_results=3)
options = vision.ImageClassifierOptions(base_options=base_options, classification_options=classification_options)
classifier = vision.ImageClassifier.create_from_options(options)


def get_random_image_path():
    shark_image_path = './data/shutterstock_derek_heasley_great_hammerhead_shark.jpg'
    pheasant_image_path = './data/pheasant.jpg'
    ibex_image_path = './data/ibex.jpg'

    image_path = random.choice([
        shark_image_path,
        pheasant_image_path,
        ibex_image_path
    ])
    return image_path



def get_tensor_image():
    
    image_path = get_random_image_path()

    # https://www.tensorflow.org/lite/api_docs/python/tflite_support/task/vision/TensorImage
    tensor_image = vision.TensorImage.create_from_file(image_path)
    return tensor_image


def get_tensor_image_from_buf(buf):
    tensor_image = vision.TensorImage.create_from_buffer(buf)
    return tensor_image




def classify_tensor_image(tensor_image):
    classification_result = classifier.classify(tensor_image)

    classifications = []
    # for sample in samples
    for classification in classification_result.classifications:
        # for option in top_classes:
        categories = []
        for category in classification.categories:
            pred_dict = {
                'index': category.index,
                'score': category.score,
                'display_name': category.display_name,
                'category_name': category.category_name,
            }
            categories.append(pred_dict)
        
        classifications.append(categories)
    

    result_dict = {
        'classifications': classifications
    }


    """
    # result structure
    ClassificationResult(
        classifications=[
            Classifications(
                categories=[
                    Category(
                        index=84,
                        score=8.029284477233887,
                        display_name='',
                        category_name='prairie chicken'
                    ),
                    Category(
                        index=81,
                        score=7.139726638793945,
                        display_name='',
                        category_name='black grouse'
                    ),
                    Category(
                        index=83,
                        score=5.040066242218018,
                        display_name='',
                        category_name='ruffed grouse'
                    )
                ],
            head_index=0, head_name='')
        ]
    )
    """
    return result_dict


def unpack_top_pred_name_score(result_dict):
    top_pred = result_dict['classifications'][0][0]
    pred_score = top_pred['score']
    pred_name = top_pred['category_name']

    #prediction_text = f'{pred_name} - {pred_score}'
    return pred_name, pred_score



if __name__ == '__main__':
    tensor_image = get_tensor_image()
    result = classify_tensor_image(tensor_image)
    print('-----------------')
    print(result)
