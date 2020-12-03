from src.syntactical_analyzer import analise


def test_queries():
    assert analise("connect /dir1/dir2;")
    assert analise("select count edges from graph(/dir3);")
    assert analise("select edges from intersect(graph(/dir4), regex(a*) );")
    assert analise("select edges from intersect(graph(/dir5), regex((a or b)?) );")
    assert analise("select edges from regex( (a.ab+.c?)* );")
    # all together
    assert analise("connect /dir1/dir2;"
                   "select count edges from graph(/dir6);"
                   "select edges from intersect(regex((a*.b*)), regex((a?.b)) );")
    assert not analise("connect /name/")  # no ;
