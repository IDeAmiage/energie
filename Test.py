# %%
from Lib.Senders.Injector import DataBase

# %%
ip_serveur = "localhost"

# %%
bd = DataBase(ip_serveur)

# %%
bd.liste()  # Renvoi la liste des bases présentes sur le serveur

# %%
nomTemplate = "MonTemplate"
bd.create_template(nomTemplate)

# %%
nomBase = "MaBase"
bd.create(nomBase, nomTemplate)

# %%
bd.liste()  # Renvoi la liste des bases présentes sur le serveur

# %%
# ADD ADDITIONAL LIB -----
from Lib.Getters.ENEDIS.get_enedis import ENEDIS
from Lib.Senders.Injector import Injection

CONFIG_ = "config.json"

e = ENEDIS(config_file=CONFIG_)
# # * Get data ---
data = e.give_measure_info()
meta = e.give_meta_info()

assert data is not None
assert meta is not None

# %%
inject = Injection(dbname="MaBase", meta=meta, df=data, ip=ip_serveur)

# %%
inject.injection()
