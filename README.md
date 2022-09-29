# DressDial
Data and generation code for the DressDial dataset. DressDial is a dataset of generated shopping dialogues about dresses. 
We employed a self-play template-guided framework to generate the dialogue automatically.

```
.
+---- example
|     +---- 457152_5_19_0.json (an exemple of generated dialogue without turn state annotation)
+---- dialog_v0_para_o/ (dir to save generated dialogues without turn state annotations)
+---- dialog_v0_para_x/ (dir to save generated dialogues with turn state annotations)
+---- dress_info.csv (information of all dresses)
+---- dream_dress_info.csv (information of dream dresses)
+---- dream_dresses.json (list of ID of dream dresses)
+---- sys_persona.json (personality of 20 systems)
+---- user_persona.json (personality of 8 users)
+---- dress_attrs_templates.csv (template of generation for each attribute/slot)
+---- generate_dataset.py
```

To generate the dataset with our proposed framework, run

> $python generate_dataset.py


