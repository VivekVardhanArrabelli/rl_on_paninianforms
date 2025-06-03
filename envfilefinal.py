{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;\red255\green255\blue255;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;\cssrgb\c100000\c100000\c100000;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs26\fsmilli13333 \cf2 \cb3 \expnd0\expndtw0\kerning0
import random\
import pandas as pd\
import vidyut\
vp = vidyut.vidyut.prakriya\
\
class SimplePaninianEnv:\
    def __init__(self, dataset_filepath):\
        df = pd.read_csv(dataset_filepath, encoding="utf-8", keep_default_na=False)\
        self.dataset = []\
        for _, row in df.iterrows():\
            self.dataset.append(\{\
                "dhatu_slp1": row["dhatu_slp1"],\
                "surface_form_vidyut": row["surface_form_vidyut"],\
                "form_metadata": \{\
                    "tense": row["tense"],\
                    "person": row["person"],\
                    "number": row["number"],\
                    "voice_for_form": row["voice_for_form"],\
                    "gana": str(row["gana"]),\
                    "root_pada_capability": row["root_pada_capability"],\
                    "settva": row["settva"]\
                \}\
            \})\
        self.current_data = None\
        self.vyakarana_engine = vp.Vyakarana()\
        self.gana_map = \{"1": vp.Gana.Bhvadi, "2": vp.Gana.Adadi, "3": vp.Gana.Juhotyadi, "4": vp.Gana.Divadi, "5": vp.Gana.Svadi, "6": vp.Gana.Tudadi, "7": vp.Gana.Rudhadi, "8": vp.Gana.Tanadi, "9": vp.Gana.Kryadi, "10": vp.Gana.Curadi\}\
        self.lakara_map = \{"present": vp.Lakara.Lat, "past": vp.Lakara.Lun, "imperative": vp.Lakara.Lot, "future": vp.Lakara.Lrt, "perfect": vp.Lakara.Lit\}\
        self.purusha_map = \{"1st": vp.Purusha.Uttama, "2nd": vp.Purusha.Madhyama, "3rd": vp.Purusha.Prathama\}\
        self.vacana_map = \{"singular": vp.Vacana.Eka, "dual": vp.Vacana.Dvi, "plural": vp.Vacana.Bahu\}\
        self.voice_map = \{"active": vp.DhatuPada.Parasmaipada, "middle": vp.DhatuPada.Atmanepada\}\
\
    def _create_observation(self):\
        meta = self.current_data["form_metadata"]\
        return \{\
            "dhatu": self.current_data["dhatu_slp1"],\
            "gana": meta["gana"],\
            "pada_root": meta["root_pada_capability"],\
            "settva": meta["settva"],\
            "target_tense": meta["tense"],\
            "target_person": meta["person"],\
            "target_number": meta["number"],\
            "target_voice_form": meta["voice_for_form"]\
        \}\
\
    def reset(self):\
        self.current_data = random.choice(self.dataset)\
        return self._create_observation()\
\
    def step(self, agent_action_str):\
        meta = self.current_data["form_metadata"]\
        dhatu_slp1 = self.current_data["dhatu_slp1"]\
        gold_surface_form = self.current_data["surface_form_vidyut"]\
\
        dhatu = vp.Dhatu.mula(dhatu_slp1, self.gana_map[meta["gana"]])\
        tinanta_args = vp.Pada.Tinanta(\
            dhatu=dhatu,\
            prayoga=vp.Prayoga.Kartari,\
            lakara=self.lakara_map[meta["tense"]],\
            purusha=self.purusha_map[meta["person"]],\
            vacana=self.vacana_map[meta["number"]],\
            dhatu_pada=self.voice_map[meta["voice_for_form"]]\
        )\
        prakriya_results = self.vyakarana_engine.derive(tinanta_args)\
        derived_form = prakriya_results[0].text if prakriya_results else gold_surface_form\
\
        reward = 1.0 if agent_action_str.strip() == derived_form.strip() else 0.0\
\
        done = True\
        next_observation = None\
        info = \{"gold": derived_form, "predicted": agent_action_str\}\
        return next_observation, reward, done, info\
\
    def render(self):\
        pass}