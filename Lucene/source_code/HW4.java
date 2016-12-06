import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class HW4 {
	private static Analyzer analyzer = new SimpleAnalyzer(Version.LUCENE_47);

	private IndexWriter writer;
	private ArrayList<File> queue = new ArrayList<File>();

	public static void main(String[] args) throws IOException {
		System.out.println("Enter the relative path of the source_code folder");
		String indexLocation = null;
		Scanner sc = new Scanner(System.in);
		String resourceDir = sc.nextLine();
		sc.close();
		System.out.println("the path provided is " + resourceDir);
		HW4 indexer = null;
		try {
			indexLocation = resourceDir + "\\lucene_index_files";
			indexer = new HW4(indexLocation);
		} catch (Exception ex) {
			System.out.println("Cannot create index..." + ex.getMessage());
			System.exit(-1);
		}

		try {
			// try to add file into the index
			indexer.indexFileOrDirectory(resourceDir + "\\generated_corpus");
		} catch (Exception e) {
			System.out.println("Error indexing " + " : " + e.getMessage());
		}

		// ===================================================
		// after adding, we always have to call the
		// closeIndex, otherwise the index is not created
		// ===================================================
		indexer.closeIndex();

		// =========================================================
		// Now search
		// =========================================================
		IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(indexLocation)));
		IndexSearcher searcher = new IndexSearcher(reader);
		TopScoreDocCollector collector = null;

		int query_id = 1;
		Scanner queryScan = new Scanner(new File(resourceDir + "\\query.txt"));

		try {
			/* Removing index files, if any existing in the directory */
			File indexDir = new File(indexLocation);
			if (indexDir.isDirectory()) {
				for (File f : indexDir.listFiles()) {
					if (f.exists()) {
						f.delete();
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(-1);
		}

		File docFile = new File(resourceDir + "\\doc_score\\Lucene_doc_score.txt");
		FileWriter docFileWriter = new FileWriter(docFile);
		while (queryScan.hasNextLine()) {
			try {
				String currentQuery = queryScan.nextLine().toLowerCase();
				Query q = new QueryParser(Version.LUCENE_47, "contents", analyzer).parse(currentQuery);
				collector = TopScoreDocCollector.create(1000, true); //Scoring for all the documents.
				searcher.search(q, collector);
				ScoreDoc[] hits = collector.topDocs().scoreDocs;

				// 4. display results
				for (int i = 0; i < Math.min(100, hits.length); ++i) {
					int docId = hits[i].doc;
					Document d = searcher.doc(docId);
					String filename = d.get("filename");
					filename = filename.substring(0, filename.length() - 4);
					String concatenatedOutput = query_id + " Q0 " + filename + "(doc_id = " + docId + ") " + (i + 1)
							+ " " + hits[i].score + " LuceneModel\n";
					System.out.print(concatenatedOutput);
					docFileWriter.write(concatenatedOutput);
				}
				docFileWriter.write("\n\n");
				query_id++;
			} catch (Exception e) {
				e.printStackTrace();
				System.exit(-1);
			}

		}
		queryScan.close();
		docFileWriter.close();
	}

	/**
	 * Constructor
	 * 
	 * @param indexDir
	 *            the name of the folder in which the index should be created
	 * @throws java.io.IOException
	 *             when exception creating index.
	 */
	HW4(String indexDir) throws IOException {

		FSDirectory dir = FSDirectory.open(new File(indexDir));

		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47, analyzer);

		writer = new IndexWriter(dir, config);
	}

	/**
	 * Indexes a file or directory
	 * 
	 * @param fileName
	 *            the name of a text file or a folder we wish to add to the
	 *            index
	 * @throws java.io.IOException
	 *             when exception
	 */
	public void indexFileOrDirectory(String fileName) throws IOException {
		// ===================================================
		// gets the list of files in a folder (if user has submitted
		// the name of a folder) or gets a single file name (is user
		// has submitted only the file name)
		// ===================================================
		addFiles(new File(fileName));

		int originalNumDocs = writer.numDocs();
		for (File f : queue) {
			FileReader fr = null;
			try {
				Document doc = new Document();

				// ===================================================
				// add contents of file
				// ===================================================
				fr = new FileReader(f);
				doc.add(new TextField("contents", fr));
				doc.add(new StringField("path", f.getPath(), Field.Store.YES));
				doc.add(new StringField("filename", f.getName(), Field.Store.YES));

				writer.addDocument(doc);
				System.out.println("Added: " + f.getName());
			} catch (Exception e) {
				System.out.println("Could not add: " + f);
			} finally {
				fr.close();
			}
		}

		int newNumDocs = writer.numDocs();
		System.out.println("");
		System.out.println("************************");
		System.out.println((newNumDocs - originalNumDocs) + " documents added.");
		System.out.println("************************");

		queue.clear();
	}

	private void addFiles(File file) {

		if (!file.exists()) {
			System.out.println(file + " does not exist.");
		}
		if (file.isDirectory()) {
			for (File f : file.listFiles()) {
				addFiles(f);
			}
		} else {
			String filename = file.getName().toLowerCase();
			// ===================================================
			// Only index text files
			// ===================================================
			if (filename.endsWith(".htm") || filename.endsWith(".html") || filename.endsWith(".xml")
					|| filename.endsWith(".txt")) {
				queue.add(file);
			} else {
				System.out.println("Skipped " + filename);
			}
		}
	}

	/**
	 * Close the index.
	 * 
	 * @throws java.io.IOException
	 *             when exception closing
	 */
	public void closeIndex() throws IOException {
		writer.close();
	}
}