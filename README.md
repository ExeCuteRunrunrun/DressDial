# DressDial
Data and generation code for the DressDial dataset. DressDial is a dataset of generated shopping dialogues about dresses. 
We employed a self-play template-guided framework to generate the dialogue automatically.

## File structure

```
.
+---- example
|     +---- 457152_5_19_0.json (an exemple of generated dialogue without turn state annotation)
+---- dress_info.csv (information of all dresses)
+---- dream_dress_info.csv (information of dream dresses)
+---- dream_dresses.json (list of ID of dream dresses)
+---- sys_persona.json (personality of 20 systems)
+---- user_persona.json (personality of 8 users)
+---- dress_attrs_templates.csv (template of generation for each attribute/slot)
+---- generate_dataset.py
```

## Clone this repo

> $git clone git@github.com:ExeCuteRunrunrun/DressDial.git
> cd DressDial

## Create 2 folders for stock the generated files

```
+---- dialog_v0_para_o/ (dir to save generated dialogues without turn state annotations)
+---- dialog_v0_para_x/ (dir to save generated dialogues with turn state annotations)
```

> $mkdir dialog_v0_para_o
> $mkdir dialog_v0_para_x

## To generate the dataset with our proposed framework, run

> $python generate_dataset.py

For each file generated, its name follows the format of {*dream_dress_id*}\_{*user_id*}\_{*system_id*}\_{*ind*}.json.

For stupid systems (*system_id* from 0-6 and 10-16), we generate 1 dialogue each time (*ind*=0).

For clever systems (*system_id* from 7-9 and 17-19), we generate 3 dialogues each time (*ind* from 0-2).
