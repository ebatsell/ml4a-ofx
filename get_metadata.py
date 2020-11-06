import boto3
import os

client = boto3.client('dynamodb')
image_ids = os.listdir("images")

# print(image_ids)
tsv = open("image_metadata.tsv", "a")
keys = ["id", "associated_text", "community", "community_size", "created", "current_num_comments", "current_score", "image_url"]
tsv.write(','.join(keys) + '\n')
image_metadata = []
for img_id in image_ids:
    response = client.get_item(
        TableName='meme-metadata',
        Key={'id': {'S': img_id}}
    )

    if 'Item' not in response:
        print('Image we want to update does not exist in the database, id=' + img_id)
        continue

    content = response["Item"]
    values = []
    for key in keys:
        k = 'N' if 'N' in content[key] else 'S' # for our limited fields
        values.append(content[key][k])

    tsv.write('\t'.join(values) + '\n')
    print(response)

tsv.close()
