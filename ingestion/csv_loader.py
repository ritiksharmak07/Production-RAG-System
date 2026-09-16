from pathlib import Path

import pandas as pd

from utils.document import Document


class CSVLoader:

    def load(self, file_path: str):

        file_path = Path(file_path)

        df = pd.read_csv(file_path)

        documents = []

        for index, row in df.iterrows():

            text = " | ".join(str(value) for value in row.values)

            documents.append(

                Document(

                    text=text,

                    metadata={
                        "filename": file_path.name,
                        "row": index,
                        "source": "csv"
                    }

                )

            )

        return documents