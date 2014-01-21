import common.config as cfg

from sqlalchemy import create_engine, Column, MetaData, Table
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import mapper, sessionmaker

import re, hashlib
import xml.etree.ElementTree as ET

#from db import node

class Node(object):
    pass

engine = create_engine('mysql+pymysql://'+ cfg.values["db"]["user"] + ':'+ cfg.values["db"]["password"] + '@'+ cfg.values["db"]["host"] +'/'+ cfg.values["db"]["name"])
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData(engine)
node = Table('node', metadata,
    Column('id', Integer, primary_key=True),
    Column('key', String),
    Column('name', String)
    )
mapper(Node, node)


tree = ET.parse('Data/repgen.xml')
thesaurus = tree.getroot()

for node_xml in thesaurus:
    
    # create node key
    descriptor_xml = node_xml.find('DESCRIPTOR') if node_xml.find('DESCRIPTOR') is not None else node_xml.find('NON-DESCRIPTOR')
    if descriptor_xml is not None:
        key = hashlib.md5(re.sub(r'[^a-zA-Z0-9,\.\(\)\'" /\\\-]', "", descriptor_xml.text.lower())).hexdigest()
    else:
        print node_xml
        raise Exception("no description field for root node")

    # check for existing node by key
    existing_node = session.query(Node).filter_by(key=key).all()

    print existing_node

    # add/update node data
    # enumerate node items, recurse into node item
    # ?? if main node, clear children
    # enumerate non-node items, add/update
