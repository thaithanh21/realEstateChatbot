Version 2.2:
 - Recommendation feature API is deployed in gcloud
  send post request to http://35.186.146.65/recom/v1/posts
 - API input example: *numre: maximum number of ouput aspect* 
{
	"tags":[{"content": "nhà", "type": "realestate_type"}, {"content": "quận 1", "type": "addr_district"}, {"content": "đầm sen", "type": "surrounding_name"}],
	"numre":5
}
- API output example:
{
    "bad_aspect": [
        {
            "content": "đầm sen",
            "type": "surrounding_name"
        }
    ],
    "position": [
        "mặt tiền"
    ],
    "potential": [
        "kinh doanh",
        "cho thuê"
    ],
    "surrounding": [
        "chợ"
    ],
    "surrounding_name": [
        "bến thành"
    ]
}

- Recommendation mechanic is improved compare to version 2.1
