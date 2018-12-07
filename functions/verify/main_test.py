from unittest.mock import Mock
import main

########### Integration Tests #############

def test_verify():
    import json
    data = """
    {
        "ilcId": "227ab442-398b-4d73-abf2-cc438761d8f8",
        "documentUri": "gs://veritrade/original_bill_of_loading.jpg",
        "imageUri": "gs://veritrade/lubricants.jpg"
    }
    """
    req = Mock(get_json=Mock(return_value=data))
    main.verify(req)

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

def test_query_ilc_gcloud():
    main.query_ilc_gcloud()

def test_query_ilc():
    ilc_json = main.query_ilc('227ab442-398b-4d73-abf2-cc438761d8f8')
    description_of_goods = main.parse_description_of_goods(ilc_json)
    assert description_of_goods[0] == "10 bottles of lubricants"

########## Unit Tests #############

def test_build_response():

    import json
    ilc_id = '227ab442-398b-4d73-abf2-cc438761d8f8'
    description_of_goods = '10 bottles of lubricants'
    document_hits = ['oil', 'lubricants']
    image_hits = []
    json_string = main.build_response(ilc_id, description_of_goods, document_hits, image_hits)
    dic = json.loads(json_string)
    assert dic["descriptionOfGoods"] == '10 bottles of lubricants'
    assert dic["ilcId"] == '227ab442-398b-4d73-abf2-cc438761d8f8'
    assert dic["imageVerified"] == False
    assert dic["documentVerified"] == True

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
    
def test_parse_description_of_goods():
    ilc_json = """
    {
        "id": "227ab442-398b-4d73-abf2-cc438761d8f8",
        "customerId": "AAAA0011",
        "inputBranch": null,
        "inBehalfOfBranch": null,
        "beneficiary": null,
        "amountAndConfirmationDetails": null,
        "paymentDetails": null,
        "shipmentDetails": null,
        "issuingBankName": "HSBC",
        "issuingReference": null,
        "advisingBank": {
            "name": "Bank of Ireland",
            "address": "40 Mespil Road, Dublin 4",
            "BIC": "BOFIIE2D"
        },
        "adviseThruBank": null,
        "narrativeDetails": {
            "descriptionOfGoods": {
                "lines": ["10 bottles of lubricants"]
            },
            "documentsRequired": null,
            "additionalInstructions": null,
            "specialPaymentConditionsForBeneficiary": null
        },
        "presentationDays": null,
        "presentationDaysNarrative": null,
        "requestedConfirmationPartyId": null,
        "shipmentPeriod": null,
        "additionalAmount": null,
        "bankInstructions": null
    }
    """
    description_of_goods = main.parse_description_of_goods(ilc_json)
    assert description_of_goods[0] == "10 bottles of lubricants"
