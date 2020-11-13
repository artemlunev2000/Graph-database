from src.syntactical_analyzer import analise


def test_queries():
    assert analise("connect /dir1/dir2;")
    assert analise("select count edges from graph(/dir3);")
    assert analise("select edges from intersect(graph(/dir4), regex(a*) );")
    assert not analise("connect /name/")  # no ;
