from fastapi import APIRouter

from models.config.configModel import ConfigModel

config = APIRouter(prefix="/api/config", tags=["openapi"])


@config.post("/create")
def conf_create(conf:ConfigModel):

    print(conf)
    return {"message": "创建成功"}

#
# @config.route("/select", methods=["GET"])
# def conf_select():
#     config_mytools = db.session.query(ConfigMyTools).all()
#     return jsonify(config_mytools), 200
#
#
# @config.route("/select/<conf_type>", methods=["GET"])
# def conf_select_by_conf_type(conf_type):
#     config_mytools = db.session.query(ConfigMyTools).filter_by(conf_type=conf_type).all()
#     return jsonify(config_mytools), 200
#
#
# @config.route('/delete', methods=["GET"])
# def conf_delete():
#     ConfigMyTools.query.delete()
#     db.session.commit()
#     return jsonify({"message": "删除成功"}), 200
#
#
# @config.route('/update/<int:id>', methods=['GET', "POST"])
# def conf_update(id: int):
#     conf_data = db.get_or_404(ConfigMyTools, id)
#     data = request.get_json()
#     conf_data.conf_content = data['confContent']
#     db.session.commit()
#     return jsonify({"message": "更新成功"}), 200