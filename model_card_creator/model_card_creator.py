import model_card_toolkit as mctlib
import base64
import matplotlib.pyplot as plt
from io import BytesIO
import uuid
from datetime import date


class ModelCardCreator:
    def __init__(self,
                 output_path: str,
                 model_name: str,
                 overview: str,
                 owner_name: str,
                 owner_contact_mail: str) -> None:

        self.mct = mctlib.ModelCardToolkit(output_path)
        self.model_card = self.mct.scaffold_assets()
        self.model_card.model_details.name = model_name
        self.model_card.model_details.overview = overview

        self.model_card.model_details.version.name = str(uuid.uuid4())
        self.model_card.model_details.version.date = str(date.today())

        self.model_card.model_details.references = []
        self.model_card.considerations.limitations = []
        self.model_card.considerations.ethical_considerations = []
        self.model_card.considerations.use_cases = []
        self.model_card.considerations.users = []
        self.model_card.model_parameters.data = []
        self.model_card.quantitative_analysis.performance_metrics = []

        self.model_card.model_details.owners = []
        self.add_owner(owner_name, owner_contact_mail)

    @staticmethod
    def _img_to_base64string(plot) -> str:
        img = BytesIO()
        plot.savefig(img, format="png")
        return base64.encodebytes(img.getvalue()).decode("utf-8")

    def compile_model_card(self) -> str:
        self.mct.update_model_card(self.model_card)
        return self.mct.export_format()

    def add_owner(self, name: str, contact: str) -> None:
        owner = mctlib.Owner(name=name, contact=contact)
        self.model_card.model_details.owners.append(owner)

    def add_risk_and_mitigation(self, risk_name: str, mitigation_strategy: str)-> None:
        risk = mctlib.Risk(name=risk_name, mitigation_strategy=mitigation_strategy)
        self.model_card.considerations.ethical_considerations.append(risk)

    def add_limitation(self, description: str)-> None:
        limitation = mctlib.Limitation(description=description)
        self.model_card.considerations.limitations.append(limitation)

    def add_references(self, reference_url: str)-> None:
        reference = mctlib.Reference(reference=reference_url)
        self.model_card.model_details.references.append(reference)

    def add_user(self, description: str)-> None:
        user = mctlib.User(description=description)
        self.model_card.considerations.users.append(user)

    def add_usecase(self, description: str)-> None:
        use_case = mctlib.UseCase(description=description)
        self.model_card.considerations.use_cases.append(use_case)

    def add_dataset_descriptions(self, description: str, images: list) -> None:
        dataset = mctlib.Dataset()
        dataset.graphics.description = (description)

        graphics = [mctlib.Graphic(image=self._img_to_base64string(i)) for i in images]

        dataset.graphics.collection = graphics

        self.model_card.model_parameters.data.append(dataset)

    def add_performance_metrics(self, type: str, value: str):
        self.model_card.quantitative_analysis.performance_metrics.append(
            mctlib.PerformanceMetric(type=type, value=value),
        )

    def add_metric_descriptions(self, description: str, images: list) -> None:
        self.model_card.quantitative_analysis.graphics.description = (description)
        self.model_card.quantitative_analysis.graphics.collection = [mctlib.Graphic(image=self._img_to_base64string(i)) for i in images]

