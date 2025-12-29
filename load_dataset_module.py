import os
import pandas as pd


class DataLoader:
    def __init__(self, file_name="data.csv"):
        self.data_file = file_name
        self.artist_to_tracks = {}
        self.all_songs = []
        self.all_artists = []
        self.artist_features_df = None
        self.data_ready = False

    def _parse_artists(self, artists_str):
        """Parse artist string into a list of artist names"""
        if pd.isna(artists_str) or not artists_str:
            return ["Unknown"]

        artists_str = str(artists_str).strip()

        if "," in artists_str:
            return [a.strip() for a in artists_str.split(",") if a.strip()]

        return [artists_str]

    def load_data(self):
        """Load and process CSV dataset"""
        try:
            if not os.path.exists(self.data_file):
                print(f"File not found: {self.data_file}")
                return None

            df = pd.read_csv(self.data_file)
            if df.empty:
                return None

            self.artist_to_tracks.clear()
            self.all_songs.clear()
            self.all_artists.clear()

            for _, row in df.iterrows():
                song = {
                    "id": str(row.get("id", "")),
                    "name": str(row.get("name", "")),
                    "acousticness": float(row.get("acousticness", 0)),
                    "danceability": float(row.get("danceability", 0)),
                    "energy": float(row.get("energy", 0)),
                    "liveness": float(row.get("liveness", 0)),
                    "loudness": float(row.get("loudness", 0)),
                    "popularity": float(row.get("popularity", 0)),
                    "speechiness": float(row.get("speechiness", 0)),
                    "tempo": float(row.get("tempo", 0)),
                    "valence": float(row.get("valence", 0)),
                }

                self.all_songs.append(song)

                artists = self._parse_artists(row.get("artists", ""))

                for artist in artists:
                    if artist not in self.artist_to_tracks:
                        self.artist_to_tracks[artist] = []
                        self.all_artists.append(artist)

                    self.artist_to_tracks[artist].append(song)

            self.data_ready = True
            self._create_artist_features()
            return self.artist_to_tracks

        except Exception as e:
            print("Error loading data:", e)
            return None

    def _create_artist_features(self):
        features = [
            "acousticness",
            "danceability",
            "energy",
            "liveness",
            "loudness",
            "popularity",
            "speechiness",
            "tempo",
            "valence",
        ]

        rows = []

        for artist, tracks in self.artist_to_tracks.items():
            avg = {f: 0 for f in features}

            for t in tracks:
                for f in features:
                    avg[f] += t[f]

            for f in features:
                avg[f] /= len(tracks)

            row = {"Artist_name": artist}
            for i, f in enumerate(features, 1):
                row[f"Feature{i}"] = avg[f]

            rows.append(row)

        self.artist_features_df = pd.DataFrame(rows)
        self.artist_features_df.to_csv("artist_features.csv", index=False)

    def get_artist_features_dataframe(self):
        return self.artist_features_df

    def get_all_artists(self):
        return self.all_artists