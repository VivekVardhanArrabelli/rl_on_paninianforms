{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;\red255\green255\blue255;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;\cssrgb\c100000\c100000\c100000;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs26\fsmilli13333 \cf2 \cb3 \expnd0\expndtw0\kerning0
import unittest\
import pandas as pd\
from paninian_env import SimplePaninianEnv\
\
class TestSimplePaninianEnv(unittest.TestCase):\
    def setUp(self):\
        dummy_data = [\
            \{"dhatu_slp1": "BU", "surface_form_vidyut": "Bavati", "tense": "present", "person": "3rd", "number": "singular", "voice_for_form": "active", "gana": "1", "root_pada_capability": "P", "settva": "seT"\},\
            \{"dhatu_slp1": "BU", "surface_form_vidyut": "Bavatu", "tense": "imperative", "person": "3rd", "number": "singular", "voice_for_form": "active", "gana": "1", "root_pada_capability": "P", "settva": "seT"\}\
        ]\
        df = pd.DataFrame(dummy_data)\
        df.to_csv("dummy_dataset.csv", index=False, encoding="utf-8")\
        self.env = SimplePaninianEnv(dataset_filepath="dummy_dataset.csv")\
\
    def test_reset(self):\
        observation = self.env.reset()\
        self.assertIn("dhatu", observation)\
        self.assertIn("target_tense", observation)\
        self.assertEqual(observation["dhatu"], "BU")\
\
    def test_step_correct_action(self):\
        self.env.reset()\
        _, reward, done, info = self.env.step("Bavati")\
        self.assertEqual(reward, 1.0)\
        self.assertTrue(done)\
        self.assertIn("gold", info)\
        self.assertIn("predicted", info)\
\
    def test_step_incorrect_action(self):\
        self.env.reset()\
        _, reward, done, info = self.env.step("wrong_form")\
        self.assertEqual(reward, 0.0)\
        self.assertTrue(done)\
        self.assertIn("gold", info)\
        self.assertIn("predicted", info)\
\
if __name__ == "__main__":\
    unittest.main()}