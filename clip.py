import ruclip

device = 'cuda'
clip, processor = ruclip.load('ruclip-vit-base-patch32-384', device=device)