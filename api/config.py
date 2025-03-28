from fastapi import APIRouter

from db import SessionDep
from models.config import DBConfigModel

router = APIRouter(prefix="/api/config", tags=["config"])


@router.post("/create")
def conf_create(conf:DBConfigModel, session: SessionDep):
    db_hero = DBConfigModel.model_validate(conf)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return {"message": "创建成功"}



@router.get("/select")
def conf_select(session: SessionDep):
    c = session.get()
    return c


@router.get("/select/<conf_type>")
def conf_select_by_conf_type(conf_type, session: SessionDep):
    config_mytools = session.get(ConfigModel.confType, conf_type=conf_type)
    return config_mytools
#
#
# @router.route('/delete', methods=["GET"])
# def conf_delete():
#     ConfigMyTools.query.delete()
#     db.session.commit()
#     return jsonify({"message": "删除成功"}), 200
#
#
# @router.route('/update/<int:id>', methods=['GET', "POST"])
# def conf_update(id: int):
#     conf_data = db.get_or_404(ConfigMyTools, id)
#     data = request.get_json()
#     conf_data.conf_content = data['confContent']
#     db.session.commit()
#     return jsonify({"message": "更新成功"}), 200