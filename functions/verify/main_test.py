import main

def test_verify_doc_image():
    hits = main.find_hits(
        main.detect_document_texts('gs://veritrade/original_bill_of_loading.jpg'), 
        main.detect_labels('gs://veritrade/lubricants.jpg'))
    assert len(hits) > 0

def test_verify_goods_doc():
    hits = main.find_hits(
        main.detect_entities('10 bottles of lubricants'),
        main.detect_document_texts('gs://veritrade/original_bill_of_loading.jpg'))
    assert len(hits) > 0

def test_verify_goods_image():
    hits = main.find_hits(
        main.detect_entities('10 bottles of lubricants'),
        main.detect_labels('gs://veritrade/lubricants.jpg'))
    assert len(hits) > 0

def test_the_longer_keyword():
    assert main.the_longer_keyword("lubr", "lubricant") == "lubricant"
    assert main.the_longer_keyword("them", "the") == "them"

def test_is_match():
    assert main.is_match('lubricant', 'lubricants') == True
    assert main.is_match('lubricants', 'lubricant') == True
    assert main.is_match('lu', 'lubricant') == False
    assert main.is_match('lubr', 'lubricant') == True
    assert main.is_match('them', 'the') == True
    assert main.is_match('th', 'thermos') == False

# def test_detect_entities():
    # entities = main.detect_entities("20 bags of horse manure")

# def test_detect_labels():
#     main.detect_labels('gs://veritrade/lubricants.jpg')

# def test_detect_image_texts():
#     main.detect_image_texts('gs://veritrade/Bill-of-Lading.jpg')

# def test_detect_document_texts():
#     document_keywords = main.detect_document_texts('gs://veritrade/original_bill_of_loading.jpg')
    
