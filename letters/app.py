from flask import Blueprint, request, flash, make_response, render_template
from flask_restx import Namespace, Resource, fields
from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from models import LetterTable
from datetime import datetime


letters = Blueprint("letters", __name__, template_folder="templates", static_folder="static")

ns_letters = Namespace("letters", description="Namespace for letters")

class LetterModel(BaseModel):
    content: str
    uuid: str = Field(default_factory=lambda: str(uuid4()))

letter_input = ns_letters.model("LetterInput", {
    "content": fields.String(required=True, description="Content of your letter"),
})



@ns_letters.route("/letter")
class Letter(Resource):
    @ns_letters.expect(letter_input)
    def post(self):
        try:
            data = request.json
            letter = LetterModel(**data)
            LetterTable.create(LetterContent=letter.content,
                               Uuid=letter.uuid)
            flash("Letter created", category="success")
            return {"message": "success"}, 200
        except Exception as e:
            return str(e), 400

@ns_letters.route("/inspect-letter/<string:uuid>")
class InspectLetter(Resource):
    def get(self, uuid):
        letter: LetterTable = LetterTable.get_or_none(LetterTable.Uuid == uuid)
        if not letter.IsWatched:
            letter.TimeDelete = datetime.now()
            content = letter.LetterContent
            letter.LetterContent = None
            letter.IsWatched = True
            letter.save()
            return {"message": "Success", "content": content}, 200
        else:
            timedelta = datetime.now() - letter.TimeDelete
            return f"""The letter has already been viewed {timedelta.days} days {timedelta.seconds // 3600} hours {timedelta.seconds // 60} minutes {timedelta.seconds % 60} seconds ago."""


@letters.route("/create-letter", methods=["GET"])
def create_letter():
    return make_response(render_template("letters/create_letter.html"), 200)

@letters.route("/web/letter", methods=["POST"])
def handle_letter_submission():
    try:
        content = request.form.get("content")
        letter_uuid = uuid4()

        LetterTable.create(LetterContent=content,
                               Uuid=letter_uuid)
        return render_template("letters/ready_letter.html", uuid=letter_uuid)
    except Exception as e:
        return f"Error: {str(e)}", 500

@letters.route("/web/inspect-letter/<string:uuid>", methods=["GET"])
def inspect_letter(uuid):
    letter: LetterTable = LetterTable.get_or_none(LetterTable.Uuid == uuid)

    if not letter:
        return render_template("letters/letter_not_found.html")

    if not letter.IsWatched:
        letter.TimeDelete = datetime.now()
        content = letter.LetterContent
        letter.LetterContent = None
        letter.IsWatched = True
        letter.save()
        return render_template("letters/inspect_letter.html", content=content)
    else:
        time_diff = datetime.now() - letter.TimeDelete
        return render_template("letters/already_read.html",
            minutes=time_diff.seconds // 60 % 60,
            hours=time_diff.seconds // 3600,
            seconds=time_diff.seconds % 60,
            days=time_diff.days)


def page_not_found(error):
    return render_template("letters/not_found.html"), 404