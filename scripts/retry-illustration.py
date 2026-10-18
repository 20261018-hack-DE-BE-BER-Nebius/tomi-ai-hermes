"""Bounded, visually selected figure crops for the sampled illustration, preserving source geometry."""
from dataclasses import replace
from datetime import UTC, datetime
from io import BytesIO
import json
from pathlib import Path
from PIL import Image
from tomi_ai_hermes.config import Config
from tomi_ai_hermes.domain.evidence import Document, sha256
from tomi_ai_hermes.infrastructure.core import CoreClient
from tomi_ai_hermes.infrastructure.store import EvidenceStore

config = replace(Config.from_env(), parse_max_tokens=2048)
manifest = json.loads(config.manifest_path.read_text())
page = next(row for row in manifest['pages'] if row['row_index'] == 2243)
original = (config.data_dir/'images'/page['filename']).read_bytes()
assert sha256(original) == page['image_sha256']
image = Image.open(BytesIO(original)).convert('RGB')
regions = [(0,0,300,330), (300,0,600,330), (0,330,600,600), (0,600,600,815)]
core = CoreClient(config)
receipt = {'original_page_id':page['page_id'], 'original_image_sha256':sha256(original),
           'original_width':image.width,'original_height':image.height,'method':'visually_selected_figure_regions',
           'received_at':datetime.now(UTC).isoformat(),'regions':[]}
texts = []
for index, box in enumerate(regions):
    stream = BytesIO();image.crop(box).save(stream,format='JPEG',quality=95)
    content = stream.getvalue()
    response = core.parse(content)
    choice = response['choices'][0]
    receipt['regions'].append({'index':index,'crop_image_sha256':sha256(content),'crop_box':box,
       'coordinates':'original_pixels_top_left','transform_crop_to_page':[1,0,box[0],0,1,box[1]],
       'status':'truncated' if choice.get('finish_reason')=='length' else 'partial_illustration_ocr',
       'response':response})
    if choice.get('finish_reason') != 'length' and choice['message']['content'].strip():
        texts.append(choice['message']['content'])
    (config.data_dir/'parse-receipts'/f'2243-crop-{index}.json').write_text(json.dumps(receipt['regions'][-1],ensure_ascii=False))
serialized = json.dumps(receipt,sort_keys=True)
(config.data_dir/'parse-receipts'/('2243-aggregate-'+sha256(serialized)[:12]+'.json')).write_text(json.dumps(receipt,ensure_ascii=False))
if len(texts) == len(regions):
    text = '\n\n'.join(texts)
    document = Document(document_id=page['page_id'],title='Illustrated plate, sampled row 2243',corpus='britannica',
       text=text,source_url=manifest['source_url'],revision_id=manifest['revision'],text_sha256=sha256(text),
       dataset_revision=manifest['revision'],license='CC0-1.0; National Library of Scotland',
       acquired_at=receipt['received_at'],parser_receipt_sha256=sha256(serialized),source_kind='illustration',
       parse_status='partial_illustration_ocr')
    EvidenceStore(config.data_dir/'lancedb',config.embed_dimensions,config.embed_model,config.embed_revision).save(document)
receipt['accepted_regions'] = len(texts)
receipt['document_saved'] = len(texts) == len(regions)
Path('evidence/illustration-crop-retry.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False))
print({'accepted_regions':len(texts),'document_saved':receipt['document_saved']})
