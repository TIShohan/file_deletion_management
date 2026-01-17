{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "0db6bbd0-35b3-41f9-8756-016166d57d37",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "🔍 Scanning files...\n",
      "🔍 Finding duplicates (quick scan)...\n",
      "🔍 Found 3241 potential duplicate files\n",
      "\n",
      "📁 Total files scanned: 5101\n",
      "💾 Total size: 40.32 GB\n"
     ]
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "ee64d0374e684eabad6d92d331a38282",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "HTML(value='<h4>📊 Top 10 Largest Folders</h4>')"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Folder</th>\n",
       "      <th>Total_Size_MB</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>I:\\\\Mahabub OLD LAPTOP\\tarek master\\mithu baai...</td>\n",
       "      <td>5.38 GB</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>I:\\\\Mahabub OLD LAPTOP\\tarek master\\mithu baai...</td>\n",
       "      <td>4.57 GB</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>I:\\\\Mahabub OLD LAPTOP\\New folder</td>\n",
       "      <td>2.49 GB</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>I:\\\\Mahabub OLD LAPTOP\\old project</td>\n",
       "      <td>2.49 GB</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>I:\\\\Mahabub OLD LAPTOP\\tarek master\\ADVANCE CAD.3</td>\n",
       "      <td>1.71 GB</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>I:\\\\Mahabub OLD LAPTOP\\tarek master\\Sabbir n\\Z...</td>\n",
       "      <td>1.62 GB</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>I:\\\\Mahabub OLD LAPTOP\\tarek master\\Sabbir n</td>\n",
       "      <td>1.55 GB</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>I:\\\\</td>\n",
       "      <td>1.38 GB</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>I:\\\\Mahabub OLD LAPTOP\\Soft</td>\n",
       "      <td>1.25 GB</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>I:\\\\Mahabub OLD LAPTOP\\tarek master\\soft 31.08...</td>\n",
       "      <td>1.07 GB</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                              Folder Total_Size_MB\n",
       "0  I:\\\\Mahabub OLD LAPTOP\\tarek master\\mithu baai...       5.38 GB\n",
       "1  I:\\\\Mahabub OLD LAPTOP\\tarek master\\mithu baai...       4.57 GB\n",
       "2                  I:\\\\Mahabub OLD LAPTOP\\New folder       2.49 GB\n",
       "3                 I:\\\\Mahabub OLD LAPTOP\\old project       2.49 GB\n",
       "4  I:\\\\Mahabub OLD LAPTOP\\tarek master\\ADVANCE CAD.3       1.71 GB\n",
       "5  I:\\\\Mahabub OLD LAPTOP\\tarek master\\Sabbir n\\Z...       1.62 GB\n",
       "6       I:\\\\Mahabub OLD LAPTOP\\tarek master\\Sabbir n       1.55 GB\n",
       "7                                               I:\\\\       1.38 GB\n",
       "8                        I:\\\\Mahabub OLD LAPTOP\\Soft       1.25 GB\n",
       "9  I:\\\\Mahabub OLD LAPTOP\\tarek master\\soft 31.08...       1.07 GB"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "45aeba1664c84f1c95c05f715fef2bbb",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Output(outputs=({'name': 'stdout', 'text': '✅ Scan complete! Found 5101 files\\n', 'output_type': 'stream'},))"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "95ae1234344f49c6ba6604140f3ca06e",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "HTML(value='<hr><h3>🔧 Filters</h3>')"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "cc9bfe709a824f15a22c69279bf9af8d",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "HBox(children=(Text(value='', description='Search:', placeholder='Enter filename or extension', style=TextStyl…"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "c992106c4c0f4ddca7f6362a49ceacde",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "HBox(children=(IntSlider(value=1, description='Min size (MB):', max=2214, style=SliderStyle(description_width=…"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "f3048b3fec7a402690bb653be7160464",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Checkbox(value=False, description='Show only duplicates')"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "c85e7c41c019404ca81a7dd207fae727",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Button(button_style='primary', description='🔄 Refresh List', style=ButtonStyle())"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "a368dfb6681a4811ae78cc3f14bda017",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Label(value='')"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "e824c81b56af4188939675f58c8246bf",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "HTML(value='<hr><h3>📂 Files (Select to Delete)</h3>')"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "34a742d9dd4d4a8a81aeca9ef0c00e71",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "HBox(children=(Button(button_style='success', description='✅ Select All', style=ButtonStyle()), Button(button_…"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "a307ec9822834d94891ef82e23262d79",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "HTML(value='')"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "11cff3b4a1ab4ac9b3fa2120cdcc546a",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "VBox()"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "69adf2ea47614d7ab1b355ce7e243600",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "HTML(value='<hr><h3>⚙️ Actions</h3>')"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "954041e52fc74ee9a3c950e5a0f35cd6",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Button(button_style='info', description='🔍 Dry Run', style=ButtonStyle())"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "a90d57d15c0a47ad9725258d6c9e15b3",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Output()"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "4ca2f3a923be40ef8e45794fed2967b3",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "HTML(value='<hr>')"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "b038b7419a874a21a0d57792bc4c6208",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Checkbox(value=True, description='Move to Recycle Bin (safer)')"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "2677a2b89d1e472f8bb2e1ec7e43318b",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Checkbox(value=False, description='I understand these files will be deleted')"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "8430e9e2c72c49a59272dc58e42385a1",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Button(button_style='danger', description='🔥 DELETE FILES', style=ButtonStyle())"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "861f7847f2874b3db83db74e51007b1b",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Output()"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import os\n",
    "import pandas as pd\n",
    "import ipywidgets as widgets\n",
    "from IPython.display import display, clear_output\n",
    "from datetime import datetime, timedelta\n",
    "import hashlib\n",
    "from pathlib import Path\n",
    "\n",
    "# ===================== SETTINGS =====================\n",
    "ROOT_PATH = r\"I:\\\\\"\n",
    "MAX_FILES_TO_SHOW = 100   # increased limit\n",
    "SKIP_EXTENSIONS = {'.sys', '.dll', '.exe', '.ini'}  # system files to skip\n",
    "FOCUS_EXTENSIONS = {'.tmp', '.log', '.bak', '.cache', '.old'}  # common junk files\n",
    "# ===================================================\n",
    "\n",
    "# -------- Helper Functions --------\n",
    "def format_size(size_mb):\n",
    "    \"\"\"Format size in MB or GB\"\"\"\n",
    "    if size_mb > 1024:\n",
    "        return f\"{size_mb/1024:.2f} GB\"\n",
    "    return f\"{size_mb:.2f} MB\"\n",
    "\n",
    "def get_file_age_days(path):\n",
    "    \"\"\"Get file age in days\"\"\"\n",
    "    try:\n",
    "        mtime = os.path.getmtime(path)\n",
    "        age = (datetime.now() - datetime.fromtimestamp(mtime)).days\n",
    "        return age\n",
    "    except:\n",
    "        return 0\n",
    "\n",
    "def file_hash(path, quick=True):\n",
    "    \"\"\"Generate file hash for duplicate detection\"\"\"\n",
    "    try:\n",
    "        hasher = hashlib.md5()\n",
    "        with open(path, 'rb') as f:\n",
    "            if quick:\n",
    "                # Quick hash: first 64KB only\n",
    "                hasher.update(f.read(65536))\n",
    "            else:\n",
    "                # Full file hash\n",
    "                while chunk := f.read(8192):\n",
    "                    hasher.update(chunk)\n",
    "        return hasher.hexdigest()\n",
    "    except:\n",
    "        return None\n",
    "\n",
    "# -------- Scan files --------\n",
    "print(\"🔍 Scanning files...\")\n",
    "scan_output = widgets.Output()\n",
    "\n",
    "with scan_output:\n",
    "    files = []\n",
    "    file_count = 0\n",
    "    for root, dirs, filenames in os.walk(ROOT_PATH):\n",
    "        for f in filenames:\n",
    "            try:\n",
    "                path = os.path.join(root, f)\n",
    "                size = os.path.getsize(path)\n",
    "                ext = Path(f).suffix.lower()\n",
    "                age_days = get_file_age_days(path)\n",
    "                \n",
    "                files.append({\n",
    "                    \"File\": f,\n",
    "                    \"Path\": path,\n",
    "                    \"Folder\": root,\n",
    "                    \"Size_MB\": round(size / (1024 * 1024), 2),\n",
    "                    \"Extension\": ext,\n",
    "                    \"Age_Days\": age_days,\n",
    "                    \"Modified\": datetime.fromtimestamp(os.path.getmtime(path)).strftime(\"%Y-%m-%d %H:%M\")\n",
    "                })\n",
    "                file_count += 1\n",
    "                if file_count % 1000 == 0:\n",
    "                    clear_output(wait=True)\n",
    "                    print(f\"📊 Scanned {file_count} files...\")\n",
    "            except Exception:\n",
    "                pass\n",
    "    \n",
    "    clear_output(wait=True)\n",
    "    print(f\"✅ Scan complete! Found {file_count} files\")\n",
    "\n",
    "df = pd.DataFrame(files).sort_values(\"Size_MB\", ascending=False).reset_index(drop=True)\n",
    "\n",
    "# -------- Find duplicates --------\n",
    "print(\"🔍 Finding duplicates (quick scan)...\")\n",
    "df['Hash'] = df['Path'].apply(file_hash)\n",
    "duplicates = df[df.duplicated(subset=['Hash'], keep=False) & df['Hash'].notna()]\n",
    "print(f\"🔍 Found {len(duplicates)} potential duplicate files\")\n",
    "\n",
    "# -------- Folder summary --------\n",
    "folder_summary = (\n",
    "    df.groupby(\"Folder\")[\"Size_MB\"]\n",
    "    .sum()\n",
    "    .sort_values(ascending=False)\n",
    "    .reset_index()\n",
    "    .rename(columns={\"Size_MB\": \"Total_Size_MB\"})\n",
    ")\n",
    "folder_summary['Total_Size_MB'] = folder_summary['Total_Size_MB'].apply(format_size)\n",
    "\n",
    "print(f\"\\n📁 Total files scanned: {len(df)}\")\n",
    "print(f\"💾 Total size: {format_size(df['Size_MB'].sum())}\")\n",
    "display(widgets.HTML(\"<h4>📊 Top 10 Largest Folders</h4>\"))\n",
    "display(folder_summary.head(10))\n",
    "\n",
    "# -------- Filter Controls --------\n",
    "search_box = widgets.Text(\n",
    "    description=\"Search:\",\n",
    "    placeholder=\"Enter filename or extension\",\n",
    "    style={'description_width': '80px'}\n",
    ")\n",
    "\n",
    "min_size_slider = widgets.IntSlider(\n",
    "    description=\"Min size (MB):\",\n",
    "    min=0,\n",
    "    max=int(df['Size_MB'].max()) if len(df) > 0 else 1000,\n",
    "    value=1,\n",
    "    style={'description_width': '80px'}\n",
    ")\n",
    "\n",
    "age_filter = widgets.Dropdown(\n",
    "    description=\"File age:\",\n",
    "    options=[\n",
    "        ('All files', 0),\n",
    "        ('Older than 7 days', 7),\n",
    "        ('Older than 30 days', 30),\n",
    "        ('Older than 90 days', 90),\n",
    "        ('Older than 180 days', 180),\n",
    "        ('Older than 1 year', 365)\n",
    "    ],\n",
    "    value=0,\n",
    "    style={'description_width': '80px'}\n",
    ")\n",
    "\n",
    "ext_filter = widgets.Dropdown(\n",
    "    description=\"File type:\",\n",
    "    options=['All'] + sorted(df['Extension'].unique().tolist()),\n",
    "    value='All',\n",
    "    style={'description_width': '80px'}\n",
    ")\n",
    "\n",
    "show_duplicates = widgets.Checkbox(\n",
    "    description=\"Show only duplicates\",\n",
    "    value=False\n",
    ")\n",
    "\n",
    "# -------- File display --------\n",
    "checkboxes = []\n",
    "paths = []\n",
    "file_container = widgets.VBox([])\n",
    "\n",
    "def update_file_list(_=None):\n",
    "    \"\"\"Update the file list based on filters\"\"\"\n",
    "    global checkboxes, paths\n",
    "    \n",
    "    # Apply filters\n",
    "    filtered_df = df.copy()\n",
    "    \n",
    "    # Search filter\n",
    "    if search_box.value:\n",
    "        search_term = search_box.value.lower()\n",
    "        filtered_df = filtered_df[\n",
    "            filtered_df['File'].str.lower().str.contains(search_term, na=False) |\n",
    "            filtered_df['Extension'].str.lower().str.contains(search_term, na=False)\n",
    "        ]\n",
    "    \n",
    "    # Size filter\n",
    "    filtered_df = filtered_df[filtered_df['Size_MB'] >= min_size_slider.value]\n",
    "    \n",
    "    # Age filter\n",
    "    if age_filter.value > 0:\n",
    "        filtered_df = filtered_df[filtered_df['Age_Days'] >= age_filter.value]\n",
    "    \n",
    "    # Extension filter\n",
    "    if ext_filter.value != 'All':\n",
    "        filtered_df = filtered_df[filtered_df['Extension'] == ext_filter.value]\n",
    "    \n",
    "    # Duplicates filter\n",
    "    if show_duplicates.value:\n",
    "        filtered_df = filtered_df[filtered_df['Hash'].isin(duplicates['Hash'])]\n",
    "    \n",
    "    # Create checkboxes\n",
    "    checkboxes = []\n",
    "    paths = []\n",
    "    \n",
    "    for _, row in filtered_df.head(MAX_FILES_TO_SHOW).iterrows():\n",
    "        dup_marker = \" 🔄\" if row['Hash'] in duplicates['Hash'].values else \"\"\n",
    "        cb = widgets.Checkbox(\n",
    "            description=f\"{format_size(row['Size_MB'])} | {row['File']} | {row['Modified']} ({row['Age_Days']}d){dup_marker}\",\n",
    "            indent=False,\n",
    "            layout=widgets.Layout(width='100%')\n",
    "        )\n",
    "        cb.observe(update_total, 'value')\n",
    "        checkboxes.append(cb)\n",
    "        paths.append(row[\"Path\"])\n",
    "    \n",
    "    file_container.children = checkboxes\n",
    "    results_label.value = f\"Showing {len(checkboxes)} of {len(filtered_df)} matching files\"\n",
    "    update_total()\n",
    "\n",
    "# Attach observers\n",
    "search_box.observe(update_file_list, 'value')\n",
    "min_size_slider.observe(update_file_list, 'value')\n",
    "age_filter.observe(update_file_list, 'value')\n",
    "ext_filter.observe(update_file_list, 'value')\n",
    "show_duplicates.observe(update_file_list, 'value')\n",
    "\n",
    "results_label = widgets.Label()\n",
    "\n",
    "# -------- Selection Controls --------\n",
    "def select_all(_):\n",
    "    for cb in checkboxes:\n",
    "        cb.value = True\n",
    "\n",
    "def deselect_all(_):\n",
    "    for cb in checkboxes:\n",
    "        cb.value = False\n",
    "\n",
    "select_all_btn = widgets.Button(description=\"✅ Select All\", button_style=\"success\")\n",
    "deselect_all_btn = widgets.Button(description=\"❌ Deselect All\", button_style=\"warning\")\n",
    "select_all_btn.on_click(select_all)\n",
    "deselect_all_btn.on_click(deselect_all)\n",
    "\n",
    "# -------- Total size display --------\n",
    "total_label = widgets.HTML()\n",
    "\n",
    "def update_total(_=None):\n",
    "    selected_size = sum(\n",
    "        df[df['Path'] == paths[i]]['Size_MB'].values[0] \n",
    "        for i, cb in enumerate(checkboxes) if cb.value and i < len(paths)\n",
    "    )\n",
    "    selected_count = sum(1 for cb in checkboxes if cb.value)\n",
    "    total_label.value = f\"<b>Selected: {selected_count} files | {format_size(selected_size)}</b>\"\n",
    "\n",
    "# -------- Output areas --------\n",
    "dry_output = widgets.Output()\n",
    "delete_output = widgets.Output()\n",
    "\n",
    "# -------- Dry run --------\n",
    "def dry_run(_):\n",
    "    with dry_output:\n",
    "        dry_output.clear_output()\n",
    "        print(\"🟡 DRY RUN — NO FILES WILL BE DELETED\\n\")\n",
    "        selected = [paths[i] for i, cb in enumerate(checkboxes) if cb.value]\n",
    "        if not selected:\n",
    "            print(\"No files selected.\")\n",
    "            return\n",
    "        \n",
    "        total_size = sum(\n",
    "            df[df['Path'] == p]['Size_MB'].values[0] \n",
    "            for p in selected\n",
    "        )\n",
    "        print(f\"📊 {len(selected)} files would be deleted\")\n",
    "        print(f\"💾 Total size: {format_size(total_size)}\\n\")\n",
    "        \n",
    "        for p in selected:\n",
    "            print(\"Would delete:\", p)\n",
    "\n",
    "# -------- Delete --------\n",
    "use_recycle = widgets.Checkbox(\n",
    "    description=\"Move to Recycle Bin (safer)\",\n",
    "    value=True\n",
    ")\n",
    "\n",
    "confirm_box = widgets.Checkbox(\n",
    "    description=\"I understand these files will be deleted\"\n",
    ")\n",
    "\n",
    "def delete_files(_):\n",
    "    with delete_output:\n",
    "        delete_output.clear_output()\n",
    "        if not confirm_box.value:\n",
    "            print(\"❌ Please confirm deletion.\")\n",
    "            return\n",
    "        \n",
    "        selected = [paths[i] for i, cb in enumerate(checkboxes) if cb.value]\n",
    "        if not selected:\n",
    "            print(\"No files selected.\")\n",
    "            return\n",
    "        \n",
    "        total_size = sum(\n",
    "            df[df['Path'] == p]['Size_MB'].values[0] \n",
    "            for p in selected\n",
    "        )\n",
    "        print(f\"🔥 Deleting {len(selected)} files ({format_size(total_size)})...\\n\")\n",
    "        \n",
    "        success_count = 0\n",
    "        fail_count = 0\n",
    "        \n",
    "        for p in selected:\n",
    "            try:\n",
    "                if use_recycle.value:\n",
    "                    # Try to use send2trash if available\n",
    "                    try:\n",
    "                        import send2trash\n",
    "                        send2trash.send2trash(p)\n",
    "                        print(f\"♻️  Moved to recycle bin: {p}\")\n",
    "                    except ImportError:\n",
    "                        print(\"⚠️  send2trash not installed, using permanent delete\")\n",
    "                        os.remove(p)\n",
    "                        print(f\"✅ Deleted: {p}\")\n",
    "                else:\n",
    "                    os.remove(p)\n",
    "                    print(f\"✅ Deleted: {p}\")\n",
    "                success_count += 1\n",
    "            except Exception as e:\n",
    "                print(f\"❌ Failed: {p} -> {e}\")\n",
    "                fail_count += 1\n",
    "        \n",
    "        print(f\"\\n📊 Summary: {success_count} deleted, {fail_count} failed\")\n",
    "        \n",
    "        # Update the file list\n",
    "        update_file_list()\n",
    "\n",
    "# -------- Buttons --------\n",
    "dry_button = widgets.Button(description=\"🔍 Dry Run\", button_style=\"info\")\n",
    "delete_button = widgets.Button(description=\"🔥 DELETE FILES\", button_style=\"danger\")\n",
    "refresh_button = widgets.Button(description=\"🔄 Refresh List\", button_style=\"primary\")\n",
    "\n",
    "dry_button.on_click(dry_run)\n",
    "delete_button.on_click(delete_files)\n",
    "refresh_button.on_click(update_file_list)\n",
    "\n",
    "# -------- Display --------\n",
    "display(scan_output)\n",
    "display(widgets.HTML(\"<hr><h3>🔧 Filters</h3>\"))\n",
    "display(widgets.HBox([search_box, ext_filter]))\n",
    "display(widgets.HBox([min_size_slider, age_filter]))\n",
    "display(show_duplicates)\n",
    "display(refresh_button)\n",
    "display(results_label)\n",
    "\n",
    "display(widgets.HTML(\"<hr><h3>📂 Files (Select to Delete)</h3>\"))\n",
    "display(widgets.HBox([select_all_btn, deselect_all_btn]))\n",
    "display(total_label)\n",
    "display(file_container)\n",
    "\n",
    "display(widgets.HTML(\"<hr><h3>⚙️ Actions</h3>\"))\n",
    "display(dry_button)\n",
    "display(dry_output)\n",
    "\n",
    "display(widgets.HTML(\"<hr>\"))\n",
    "display(use_recycle)\n",
    "display(confirm_box)\n",
    "display(delete_button)\n",
    "display(delete_output)\n",
    "\n",
    "# Initial load\n",
    "update_file_list()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
