import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("score_layout", ROOT / "scripts" / "score_layout.py")
score_layout = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(score_layout)


def sample_photos():
    return [
        {
            "id": chr(65 + i),
            "direction": i * 10,
            "shape": ["ridge", "diagonal"] if i % 2 == 0 else ["horizontal"],
            "colors": ["white", "blue"] if i % 2 == 0 else ["green", "red"],
            "elements": ["mountain"] if i < 5 else ["temple"],
            "right_edge": {"direction": 30, "shape": ["ridge"], "colors": ["white"]},
            "left_edge": {"direction": 30, "shape": ["ridge"], "colors": ["white"]},
            "top_edge": {"direction": 0, "elements": ["cloud"]},
            "bottom_edge": {"direction": 0, "elements": ["cloud"]},
        }
        for i in range(9)
    ]


class ScoreLayoutTests(unittest.TestCase):
    def test_direction_is_orientation_not_compass_heading(self):
        self.assertAlmostEqual(score_layout.direction_score(32, 30), 5.0 * (1 - 2 / 90))
        self.assertEqual(score_layout.direction_score(None, 30), 0.0)

    def test_tag_score_jaccard(self):
        self.assertAlmostEqual(score_layout.tag_score(["snow", "blue"], ["snow", "white"]), 5 / 3)
        self.assertEqual(score_layout.tag_score([], ["snow"]), 0.0)

    def test_edge_specific_metadata_overrides_whole_photo(self):
        a, b = sample_photos()[:2]
        score, details = score_layout.score_edges(a, b, "horizontal")
        self.assertEqual(details["direction"], 5.0)
        self.assertEqual(details["shape"], 5.0)
        self.assertGreater(score, 0.0)

    def test_adjacency_has_twelve_pairs(self):
        ids = list("ABCDEFGHI")
        pairs = list(score_layout.adjacency_pairs(ids))
        self.assertEqual(len(pairs), 12)
        self.assertEqual(pairs[0], ("A", "B", "horizontal"))
        self.assertIn(("A", "D", "vertical"), pairs)

    def test_requires_nine_unique_photos(self):
        with self.assertRaises(ValueError):
            score_layout.score_all(sample_photos()[:8], 1)
        photos = sample_photos()
        photos[1]["id"] = photos[0]["id"]
        with self.assertRaises(ValueError):
            score_layout.score_all(photos, 1)

    def test_returns_requested_top_layouts_and_edge_details(self):
        results = score_layout.score_all(sample_photos(), 2)
        self.assertEqual(len(results), 2)
        self.assertEqual([len(row) for row in results[0]["layout"]], [3, 3, 3])
        self.assertEqual(len(results[0]["edges"]), 12)
        self.assertIn("details", results[0]["edges"][0])

    def test_rejects_zero_top_k(self):
        with self.assertRaises(ValueError):
            score_layout.score_all(sample_photos(), 0)


if __name__ == "__main__":
    unittest.main()
