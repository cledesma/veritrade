def verify(request):

    request_json = request.get_json(silent=True)
    if request_json \
        and 'ilcId' in request_json \
        and 'documentUri' in request_json \
        and 'imageUri' in request_json:

        ilc_id = request_json['ilcId']
        document_image_uri = request_json['documentUri']
        goods_image_uri = request_json['imageUri']

        print('\n')
        print('=' * 20)
        print(u'{:<16}: {}'.format('ILC ID', ilc_id))
        print(u'{:<16}: {}'.format('DOC_URI', document_image_uri))
        print(u'{:<16}: {}'.format('IMAGE_URI', image_uri))
        print('=' * 20)

        ilc_json = query_ilc(ilc_id)
        description_of_goods = parse_description_of_goods(ilc_json)

def detect_entities(goods_declaration):

    from google.cloud import language_v1
    from google.cloud.language_v1 import types
    from google.cloud.language_v1 import enums
    import six

    content = goods_declaration
    client = language_v1.LanguageServiceClient()
    if isinstance (content, six.binary_type):
        content = content.decode('utf-8')
    document = {'type':  enums.Document.Type.PLAIN_TEXT, 'content': content}

    entities = client.analyze_entities(document).entities
    # entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION', 
    #     'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
    print('\n')
    print('=' * 20)
    print("Entities")
    print('=' * 20)
    result = []
    for entity in entities:
        result.append(entity.name)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('salience', entity.salience))
    return result

def detect_labels(goods_image_uri):

    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = goods_image_uri
    labels = client.label_detection(image=image).label_annotations
    print('\n')
    print('=' * 20)
    print("Labels")
    print('=' * 20)
    result = []
    for label in labels:
        result.append(label.description)
        print(label.description)
        print(label.score)
    return result

def detect_image_texts(image_uri):

    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = image_uri
    texts = client.text_detection(image=image).text_annotations
    print("\n")
    print('=' * 20)
    print("Image Text")
    print('=' * 20)
    for text in texts:
        print(text.description)
    return texts

def detect_document_texts(document_image_uri):

    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = document_image_uri
    response = client.document_text_detection(image=image)
    paragraphs = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                par = ""
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    par += word_text + " "
                paragraphs.append(par)
    all_text = ""
    for paragraph in paragraphs:
        all_text += paragraph + "\n"
    print("\n")
    print('=' * 20)
    print("All Document Text")
    print('=' * 20)
    print(all_text )
    words_that_matter = detect_entities(all_text)
    return words_that_matter

def find_hits(keywords1, keywords2):
    hit = []
    for keyword1 in keywords1:
        for keyword2 in keywords2:
            if(is_match(keyword1, keyword2)):
                hit.append(the_longer_keyword(keyword1, keyword2))
    print("\n")
    print('=' * 20)
    print("Hit Summary")
    print('=' * 20)
    print(hit)
    return hit

def is_match(word1, word2):
    result = False
    if (word1.upper() in word2.upper()) or (word2.upper() in word1.upper()):
        if (len(word1) > 2 and len(word2) > 2): 
            result = True
    return result

def the_longer_keyword(w1, w2):
    if len(w1) >= len(w2):
        return w1
    else:
        return w2

def parse_description_of_goods(ilc_json):
    import json
    data = json.loads(ilc_json)
    narrative_details = data["narrativeDetails"]
    description_of_goods = narrative_details["descriptionOfGoods"]
    lines = description_of_goods["lines"]
    result = []
    for line in lines:
        result.append(line)
    return result

def query_ilc_gcloud():
    import requests 
    URL = "https://asia-northeast1-veritrade-224415.cloudfunctions.net/trade_innovation"
    r = requests.get(url = URL) 
    print("\n")
    print('=' * 20)
    print("Query ILC - GCloud")
    print('=' * 20)
    print(r.text)
    return r.text

def query_ilc(ilc_id):
    import requests 
    BASE_URL = "http://man-lhs7gr32:8000/tradefinance/api/import-letters-of-credit/"
    URL = BASE_URL + ilc_id
    r = requests.get(url = URL) 
    print("\n")
    print('=' * 20)
    print("Query ILC")
    print('=' * 20)
    print(r.text)
    return r.text
