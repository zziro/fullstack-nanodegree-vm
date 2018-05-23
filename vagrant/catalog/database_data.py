from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# category for Soccer
category1 = Category(name="Soccer")

session.add(category1)
session.commit()

categoryItem1 = CategoryItem(name="Soccer Goalie Gloves", description="Goalkeeper gloves provide a better grip on the ball.",
                     category=category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(name="Footwear", description="Equipment provides players with the tools they need to play soccer efficiently and safely.",
                     category=category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Shin-Guards", description="Shin-guards protect player's shins, a vulnerable part of a player's body that often gets kicked.",
                     category=category1)

session.add(categoryItem3)
session.commit()


# category for Basketball
category2 = Category(name="Basketball")

session.add(category2)
session.commit()


categoryItem1 = CategoryItem(name="Backboard", description="The backboard is the rectangular board that is placed behind the rim.",
                     category=category2)

session.add(categoryItem1)
session.commit()


categoryItem2 = CategoryItem(name="Shoes", description="Shoes are specially designed to maintain high traction on the basketball court.",
                     category=category2)

session.add(categoryItem2)
session.commit()


categoryItem3 = CategoryItem(name="The Ball", description="For professional competitions, one needs to use an inflated ball made of leather.",
                     category=category2)

session.add(categoryItem3)
session.commit()

# category for Baseball
category3 = Category(name="Baseball")

session.add(category3)
session.commit()


categoryItem1 = CategoryItem(name="Baseball Glove", description="Is a large leather glove worn by baseball players of the defending team, which assists players in catching and fielding balls hit by a batter or thrown by a teammate.",
                     category=category3)

session.add(categoryItem1)
session.commit()


categoryItem2 = CategoryItem(name="Baseball Bat", description="Is a smooth wooden or metal club used in the sport of baseball to hit the ball after it is thrown by the pitcher.",
                     category=category3)

session.add(categoryItem2)
session.commit()


categoryItem3 = CategoryItem(name="Batting Helmet", description="Is worn by batters in the game of baseball or softball. It is meant to protect the batter's head from errant pitches thrown by the pitcher.",
                     category=category3)

session.add(categoryItem3)
session.commit()

print "added category items!"
