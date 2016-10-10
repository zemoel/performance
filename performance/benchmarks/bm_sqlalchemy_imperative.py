import perf.text_runner
from six.moves import xrange

from sqlalchemy import Column, ForeignKey, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


metadata = MetaData()

Person = Table('person', metadata,
               Column('id', Integer, primary_key=True),
               Column('name', String(250), nullable=False))

Address = Table('address', metadata,
                Column('id', Integer, primary_key=True),
                Column('street_name', String(250)),
                Column('street_number', String(250)),
                Column('post_code', String(250), nullable=False),
                Column('person_id', Integer, ForeignKey('person.id')))

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite://')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
metadata.create_all(engine)


# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# add 'npeople' people to the database
def main(loops, npeople):
    total_dt = 0.0

    for loops in xrange(loops):
        # drop rows created by the previous benchmark
        cur = Person.delete()
        cur.execute()

        cur = Address.delete()
        cur.execute()

        # Run the benchmark once
        t0 = perf.perf_counter()

        for i in xrange(npeople):
            # Insert a Person in the person table
            new_person = Person.insert()
            new_person.execute(name="name %i" % i)

            # Insert an Address in the address table
            new_address = Address.insert()
            new_address.execute(post_code='%05i' % i)

        # do 'npeople' queries per insert
        for i in xrange(npeople):
            cur = Person.select()
            cur.execute()

        total_dt += (perf.perf_counter() - t0)

    return total_dt


def prepare_cmd(runner, cmd):
    cmd.extend(("--rows", str(runner.args.rows)))


if __name__ == "__main__":
    runner = perf.text_runner.TextRunner(name='sqlalchemy_imperative')
    runner.metadata['description'] = ("SQLAlchemy Imperative benchmark "
                                      "using SQLite")
    runner.prepare_subprocess_args = prepare_cmd
    runner.argparser.add_argument("--rows", type=int, default=100,
                                  help="Number of rows (default: 100)")

    args = runner.parse_args()
    runner.bench_sample_func(main, args.rows)